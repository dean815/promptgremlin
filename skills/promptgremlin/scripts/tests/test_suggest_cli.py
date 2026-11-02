import contextlib
import io
import json
import os
import shutil
import tempfile
from pathlib import Path

import guidance
from pglib import fetch
from pglib import scoreboard as S

HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[1]
FIX = HERE / "fixtures"
SNAP = FIX / "scoreboard_small.json"
LB = "https://livebench.ai/data/20261025/"
# Test-only rows the committed fixtures don't carry: Fable leads on long agentic work, and
# Sonnet is the cheaper Anthropic option on coding.
EXTRA_TABLE = ("claude-fable-5.1,77.9,90.0,95.0,85.0,80.0,84.0,85.0\n"
               "claude-sonnet-5.5,65.0,90.0,94.7,85.0,78.0,83.0,84.0\n")
EXTRA_COST = ("claude-fable-5.1,150,180,300,261,25,22,25,29,1,1,10,50,1,1,1,1,936,18,1,100,150,1,40,202,1\n"
              "claude-sonnet-5.5,62.5,90,200,116.6322,25,22,25,29,1,1,3,15,1,1,1,1,540,18,1,60,150,1,30,202,1\n")


def _skill_dir(bundled=True):
    """The real skill files, with the small fixture as the bundled snapshot."""
    d = Path(tempfile.mkdtemp())
    for name in ("sources.json", "evidence.json", "model_aliases.json"):
        shutil.copy(SKILL / name, d / name)
    for name in ("targets", "types"):
        shutil.copytree(SKILL / name, d / name)
    # Family notes from the frozen lineup, so a notes refresh doesn't change what these tests see.
    for path in (FIX / "targets").glob("*.md"):
        shutil.copy(path, d / "targets" / path.name)
    if bundled:
        shutil.copy(SNAP, d / "scoreboard.json")
    return d


def _setup(cache=True, livebench=True, bundled=True, config=None, edit=None):
    """Point every input at fixtures. The cache is filled through fetch's injectable get, and
    main runs --offline, so nothing touches the network. edit changes a copy of the snapshot."""
    global SNAP
    SNAP = FIX / "scoreboard_small.json"
    if edit:
        snap = json.loads(SNAP.read_text(encoding="utf-8"))
        edit(snap)
        SNAP = Path(tempfile.mkdtemp()) / "scoreboard.json"
        SNAP.write_text(json.dumps(snap), encoding="utf-8")
    fetch.CACHE = Path(tempfile.mkdtemp())
    os.environ[S.ENV] = SNAP.as_uri()
    guidance.SKILL_DIR = _skill_dir(bundled)
    guidance.CONFIG = guidance.SKILL_DIR / "config.json"
    if config is not None:
        guidance.CONFIG.write_text(json.dumps(config), encoding="utf-8")
    files = {}
    if cache:
        files[SNAP.as_uri()] = SNAP.read_text(encoding="utf-8")
    if livebench:
        files[LB + "table.csv"] = (FIX / "livebench_table.csv").read_text(encoding="utf-8") + EXTRA_TABLE
        files[LB + "cost.csv"] = (FIX / "livebench_cost.csv").read_text(encoding="utf-8") + EXTRA_COST
    for url, text in files.items():
        fmt = "json" if url.endswith(".json") else "csv"
        assert fetch.fetch(url, fmt, get=lambda u, t=text: t).state == "live"


def _run(*args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = guidance.main(["--suggest", "--offline", *args])
    return code, out.getvalue()


def _line(text, start):
    return next(line for line in text.splitlines() if line.startswith(start))


def test_suggest_prints_header_with_pool_and_freshness():
    _setup()
    code, text = _run("--type", "build")
    assert code == 0
    assert text.splitlines()[0].startswith("Suggest: build | pool all | snapshot 2026-10-27 (stale) | impact ")
    assert _line(text, "Best quality").startswith("Best quality (Recommended): claude-code, claude-opus-5-5")
    assert "LiveBench 2026-10-25" in _line(text, "Data:")


def test_unknown_type_or_target_exits_2():
    _setup()
    assert _run("--type", "nope")[0] == 2
    assert _run("--type", "build", "--target", "nope")[0] == 2


def test_target_restricts_pool_to_its_families():
    _setup()
    code, text = _run("--type", "build", "--target", "claude-code")
    assert code == 0
    assert "| pool target |" in text.splitlines()[0]
    for start in ("Best quality", "Best value"):
        assert ", claude-" in _line(text, start) and "gpt-" not in _line(text, start)
    # The cross-vendor line is the only place another vendor may appear: Sol clears the value
    # floor against Opus at about 1/10 the cost.
    assert _line(text, "Also consider").startswith("Also consider: codex, gpt-6-1-sol, effort medium.")


def test_long_run_switches_main_evidence_to_long_agentic():
    _setup()
    text = _run("--type", "build", "--target", "claude-code", "--run-length", "long")[1]
    best = _line(text, "Best quality")
    assert "claude-fable-5-1" in best and "LiveBench long agentic 77.9" in best


def test_session_model_and_balanced_priority():
    _setup(config={"model_priority": "balanced"})
    text = _run("--type", "build", "--target", "claude-code", "--session-model", "claude-haiku-5-5")[1]
    assert _line(text, "Best value").startswith("Best value (Recommended): claude-code, claude-sonnet-5-5")
    assert _line(text, "Session").startswith("Session: claude-code, claude-haiku-5-5 (the model you're using now)")


def test_session_model_display_name_maps_to_its_note_id():
    """SKILL.md passes the conversation's model as the host names it ("Claude Haiku 5.5")."""
    _setup()
    text = _run("--type", "build", "--target", "claude-code", "--session-model", "Claude Haiku 5.5")[1]
    assert _line(text, "Session").startswith("Session: claude-code, claude-haiku-5-5 (the model you're using now)")
    # A name no notes know passes through unchanged and is noted, not offered.
    text = _run("--type", "build", "--target", "claude-code", "--session-model", "Mystery 9")[1]
    assert _line(text, "Session").startswith("Session: Mystery 9 (the model you're using now) is not offered")
    # A context-size suffix the host shows is not part of the model's id.
    text = _run("--type", "build", "--target", "claude-code", "--session-model", "Claude Opus 5.5 1m")[1]
    assert "not offered" not in text and "claude-opus-5-5-1m" not in text


def test_plan_surface():
    _setup()
    text = _run("--type", "build", "--target", "claude-code", "--surface", "plan")[1]
    assert "of your plan" in _line(text, "Best value")


def _draft_boards(snap):
    """Test-only draft rows: Opus leads creative writing and instruction following, Sonnet leads
    French by enough that the language slot's weight flips the pick."""
    rows = {"claude-opus-5-5": (1500, 1500, 1400), "claude-sonnet-5-5": (1480, 1480, 1500)}
    keys = ("lmarena:text/creative_writing", "lmarena:text/instruction_following", "lmarena:text/french")
    for key in keys:
        snap["boards"][key] = {"top": 1500, "p30": 1400}
    for mid, elos in rows.items():
        for key, elo in zip(keys, elos):
            snap["models"][mid]["metrics"][key] = [{"effort": None, "elo": elo}]


def test_language_slot_weighs_the_language_board():
    _setup(edit=_draft_boards)
    code, text = _run("--type", "draft", "--target", "anthropic")
    assert code == 0 and text.startswith("Suggest: draft | pool target |")
    # Without a language: creative writing 0.6, instruction following 0.4. Opus leads both.
    assert _line(text, "Best quality").startswith("Best quality (Recommended): claude-opus-5-5")
    # French (any case) takes 0.2 of instruction following's weight: Sonnet 0.84 to Opus 0.8.
    text = _run("--type", "draft", "--target", "anthropic", "--language", "French")[1]
    best = _line(text, "Best quality")
    assert best.startswith("Best quality (Recommended): claude-sonnet-5-5"), text
    assert "LMArena text creative writing 1480" in best


def test_output_stays_under_budget():
    _setup()
    for args in (("--type", "build"), ("--type", "draft"), ("--type", "general"),
                 ("--type", "build", "--target", "claude-code", "--session-model", "claude-haiku-5-5",
                  "--surface", "plan")):
        code, text = _run(*args)
        assert code == 0 and len(text.rstrip("\n")) < S.BUDGET, (args, len(text))


def test_offline_with_empty_cache_uses_bundled_snapshot():
    _setup(cache=False, livebench=False)
    code, text = _run("--type", "build")
    assert code == 0
    assert text.splitlines()[0].startswith("Suggest: build | pool all | snapshot 2026-10-27 (bundled) | impact ")
    assert "LiveBench unavailable" in _line(text, "Data:")


def test_no_snapshot_at_all_exits_2():
    _setup(cache=False, livebench=False, bundled=False)
    assert _run("--type", "build")[0] == 2
