import copy
import datetime as dt
import json
import shutil
import tempfile
from pathlib import Path

from pglib import fetch
from pglib import livebench as L
from pglib import registry as R
from pglib import scoreboard as S

HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[1]
FIX = HERE / "fixtures" / "scoreboard_small.json"
REG = R.load(SKILL / "sources.json")
# A frozen copy of the family notes (Effort block and model ids), so a routine notes refresh that
# adds or drops a model doesn't fail these tests.
NOTES = HERE / "fixtures" / "targets"
NOW = dt.datetime(2026, 10, 28, 9, 0)

EVIDENCE = json.loads((SKILL / "evidence.json").read_text(encoding="utf-8"))


def _lb(score, cost):
    return {"score": score, "cost_per_task": cost, "effort": "max"}


# Test-only LiveBench numbers in the shape livebench.load returns.
LIVEBENCH = {
    "claude-opus-5-5": {"livebench:coding": _lb(96.3, 5.0308), "livebench:design": _lb(86.9, 3.0),
                        "livebench:long_agentic": _lb(72.8, 38.01)},
    "claude-sonnet-5-5": {"livebench:coding": _lb(94.7, 4.0218), "livebench:design": _lb(84.0, 2.5),
                          "livebench:long_agentic": _lb(65.0, 30.0)},
    "claude-fable-5-1": {"livebench:coding": _lb(95.0, 9.0), "livebench:design": _lb(85.0, 6.0),
                         "livebench:long_agentic": _lb(77.9, 52.0)},
    "claude-haiku-5-5": {"livebench:coding": _lb(91.4, 0.84), "livebench:design": _lb(70.0, 0.5),
                         "livebench:long_agentic": _lb(40.0, 6.0)},
    "gpt-6-1-sol": {"livebench:coding": _lb(96.0, 0.4822), "livebench:design": _lb(85.0, 0.4),
                    "livebench:long_agentic": _lb(68.7, 6.4877)},
    "gemini-3-8-flash": {"livebench:coding": _lb(90.0, 0.3)},
    "gemini-3-6-flash": {"livebench:design": _lb(60.0, 0.1)},
}
LB_LIVE = {"release": "20261025", "state": "live"}
LB_MISSING = {"release": "20261025", "state": "missing"}


def _snap(livebench=True, edit=None):
    snap = json.loads(FIX.read_text(encoding="utf-8"))
    if edit:
        edit(snap)
    return S.add_livebench(snap, LIVEBENCH) if livebench else snap


def _suggest(target="claude-code", pool="target", type_="build", slots=None, session=None,
             snap=None, lb=LB_LIVE, effort=None):
    snap = snap or _snap(lb["state"] != "missing")
    ev = S.resolve_evidence(EVIDENCE, type_, slots or {})
    cands = S.candidates(target, REG, NOTES, pool, type_)
    others = S.candidates(None, REG, NOTES, "all", type_) if pool == "target" else []
    info = S.Info(type_, pool, "2026-10-27", "cached", lb, target)
    return S.choose(cands, snap, ev, info, effort=effort, session=session, others=others)


def test_win_rate():
    assert round(S.win_rate(38), 2) == 0.55
    assert round(S.win_rate(221), 2) == 0.78
    assert S.win_rate(0) == 0.5


def test_pick_variant_exact_then_nearest():
    rows = [{"effort": "xhigh", "elo": 1769}, {"effort": "high", "elo": 1711}]
    assert S.pick_variant(rows, "high")["elo"] == 1711
    assert S.pick_variant(rows, "xhigh")["elo"] == 1769
    assert S.pick_variant(rows, "max")["elo"] == 1769
    assert S.pick_variant(rows, "low")["elo"] == 1711
    # An unlabelled row is the model's default effort.
    assert S.pick_variant([{"effort": None, "elo": 1650}, {"effort": "max", "elo": 1700}], "low", "low")["elo"] == 1650
    eci = {"score": 168.83}
    assert S.pick_variant(eci, "high") is eci


def test_scale_clamps_and_derives_livebench_boards():
    assert S.scale(1807, {"top": 1807, "p30": 1612}) == 1.0
    assert S.scale(1500, {"top": 1807, "p30": 1612}) == 0.0
    assert round(S.scale(1709.5, {"top": 1807, "p30": 1612}), 2) == 0.5
    b = S.boards(_snap())
    assert b["lmarena:webdev"] == {"top": 1807, "p30": 1612}
    # LiveBench scales against the release's best score.
    assert b["livebench:coding"] == {"top": 96.3, "p30": 0}
    # Epoch's scale is the index's own top and 30th, stored by the builder.
    assert b["epoch:eci"] == {"top": 171.2, "p30": 156.33}
    # A board with no stored scale is not guessed from our own models.
    assert "epoch:eci" not in S.boards(_snap(edit=lambda s: s["boards"].pop("epoch:eci")))


def test_resolve_evidence_applies_slots():
    ev = S.resolve_evidence(EVIDENCE, "build", {})
    assert ev["main"] == {"lmarena:webdev": 0.5} and ev["cost_suite"] == "livebench:coding"
    long = S.resolve_evidence(EVIDENCE, "build", {"run_length": "long"})
    assert long["main"] == {"livebench:long_agentic": 0.5}
    assert long["cost_suite"] == "livebench:long_agentic"
    fr = S.resolve_evidence(EVIDENCE, "draft", {"language": "french"})
    assert fr["support"] == {"lmarena:text/instruction_following": 0.2, "lmarena:text/french": 0.2}
    assert fr["main"] == {"lmarena:text/creative_writing": 0.6}


def test_quality_renormalises_and_flags_thin():
    snap = _snap()
    b = S.boards(snap)
    ev = S.resolve_evidence(EVIDENCE, "build", {})
    q, cov, used = S.quality(snap["models"]["claude-opus-5-5"], ev, b, "high")
    assert q == 1.0 and cov == 1.0
    assert [k for k, _ in used] == ["lmarena:webdev", "livebench:coding", "livebench:design"]
    # Luna has only the main metric: quality renormalises over the half of the weight it has.
    q, cov, _ = S.quality(snap["models"]["gpt-6-luna"], ev, b, "low")
    assert cov == 0.5 and round(q, 3) == round((1650 - 1612) / 195, 3)
    # Only a supporting metric: thin.
    q, cov, _ = S.quality(snap["models"]["gemini-3-6-flash"], ev, b, "medium")
    assert cov == 0.25 and cov < S.THIN
    assert S.quality({"metrics": {}}, ev, b, None)[0] is None


def test_cost_per_task_bases():
    snap = _snap()
    ev = S.resolve_evidence(EVIDENCE, "build", {})
    m = snap["models"]
    assert S.cost_per_task(m["claude-opus-5-5"], ev) == (5.0308, "livebench:coding")
    assert S.cost_per_task(m["gemini-3-6-flash"], ev) == (0.1, "token-efficiency")
    assert S.cost_per_task(m["gpt-6-luna"], ev) == ((3 * 0.25 + 2.0) / 4, "list price")
    assert S.cost_per_task(m["claude-opus-5-5"], ev, "list price") == (8.0, "list price")
    assert S.cost_per_task({"metrics": {}}, ev) == (None, None)


def test_tied_uses_main_metric_cis():
    snap = _snap()
    m = snap["models"]
    rows = lambda mid, eff: S.pick_variant(m[mid]["metrics"]["lmarena:webdev"], eff)
    assert not S.tied(rows("claude-opus-5-5", "high"), rows("claude-sonnet-5-5", "xhigh"))
    assert S.tied(rows("claude-sonnet-5-5", "xhigh"), rows("gpt-6-1-sol", "medium"))
    assert not S.tied(None, rows("gpt-6-1-sol", "medium"))


def test_candidates_target_and_all():
    cc = S.candidates("claude-code", REG, NOTES, "target", "build")
    assert {c.tool for c in cc} == {"claude-code"}
    assert {c.model for c in cc} == {"claude-fable-5-1", "claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5"}
    fam = S.candidates("anthropic", REG, NOTES, "target", "draft")
    assert {c.tool for c in fam} == {None} and len(fam) == 4
    allb = S.candidates(None, REG, NOTES, "all", "build")
    assert {"claude-code", "codex", "gemini-cli"} <= {c.tool for c in allb}
    assert ("codex", "gpt-6-1-sol") in allb and ("gemini-cli", "gemini-3-8-flash") in allb
    assert not any(c.tool == "codex" and c.model.startswith("claude") for c in allb)
    alld = S.candidates(None, REG, NOTES, "all", "draft")
    assert {c.tool for c in alld} == {None}
    assert {"claude-opus-5-5", "gpt-6-1-sol", "deepseek-v4-pro"} <= {c.model for c in alld}


def test_best_and_value_differ():
    s = _suggest()
    assert s.best.model == "claude-opus-5-5" and s.best.effort == "high"
    # Fable clears the floor too but costs more; Sonnet is the cheapest that clears it (voters
    # prefer Opus 55% of the time). Haiku is cheaper but voters prefer Opus 78% of the time.
    assert s.value.model == "claude-sonnet-5-5" and s.value.basis == "livebench:coding"
    assert S.clears(s.value, s.best)
    text = S.render(s, "api", "quality")
    assert "Best quality (Recommended): claude-code, claude-opus-5-5, effort high." in text
    assert "Best value: claude-code, claude-sonnet-5-5, effort xhigh. About 20% cheaper per task (LiveBench coding $4.02 vs $5.03)" in text
    assert "voters preferred Claude Opus 5.5 about 55% of the time" in text
    assert "LMArena WebDev 1807 (Oct 23)" in text


def test_value_is_cheapest_frontier_model_across_vendors():
    s = _suggest(target=None, pool="all")
    assert s.best.model == "claude-opus-5-5"
    assert (s.value.tool, s.value.model) == ("codex", "gpt-6-1-sol")
    assert "About 1/10 the cost per task" in S.render(s, "api", "quality")


def test_same_model_prints_only_best():
    snap = _snap()
    ev = S.resolve_evidence(EVIDENCE, "build", {})
    cands = [S.Candidate("claude-code", "claude-opus-5-5"), S.Candidate("claude-code", "claude-fable-5-1")]
    s = S.choose(cands, snap, ev, S.Info("build", "target", "2026-10-27", "cached", LB_LIVE))
    assert s.value is None
    text = S.render(s, "api", "quality")
    assert "Best value: same as best quality." in text
    assert text.count("claude-opus-5-5") == 1


def test_tied_cheaper_model_is_value_and_says_so():
    def tie_haiku(snap):
        snap["models"]["claude-haiku-5-5"]["metrics"]["lmarena:webdev"] = [
            {"effort": "high", "elo": 1560, "lo": 1500, "hi": 1800, "votes": 400}]
    s = _suggest(snap=_snap(edit=tie_haiku))
    # Voters prefer Opus about 80% of the time, past the floor, but the CIs overlap.
    assert s.value.model == "claude-haiku-5-5" and S.win_rate(1807 - 1560) > S.VALUE_WIN
    assert "claude-haiku-5-5" in s.ties
    assert "statistically tied" in S.render(s, "api", "quality")


def test_balanced_priority_recommends_value():
    text = S.render(_suggest(), "api", "balanced")
    assert "Best quality: claude-code, claude-opus-5-5" in text
    assert "Best value (Recommended): claude-code, claude-sonnet-5-5" in text


def test_plan_surface_phrases_cost_as_plan_usage():
    text = S.render(_suggest(), "plan", "quality")
    assert "Uses about 20% less of your plan" in text


def test_also_consider_only_when_margin_passes():
    s = _suggest()
    assert (s.also.tool, s.also.model) == ("codex", "gpt-6-1-sol")
    assert "Also consider: codex, gpt-6-1-sol, effort medium." in S.render(s, "api", "quality")

    lb = copy.deepcopy(LIVEBENCH)
    lb["gpt-6-1-sol"]["livebench:coding"]["cost_per_task"] = 3.5
    snap = json.loads(FIX.read_text(encoding="utf-8"))
    s = _suggest(snap=S.add_livebench(snap, lb))
    assert s.also is None
    assert "Also consider: none." in S.render(s, "api", "quality")
    assert _suggest(target=None, pool="all").also is None


def test_also_consider_names_a_clearly_better_model_whatever_its_cost():
    """Codex's best is GPT-6.1 Sol; Opus is more than XV_QUALITY_GAP better on the 0-1 scale, so
    it shows although it costs about 10x as much (the cost branch caps at XV_COST_RATIO)."""
    s = _suggest(target="codex")
    assert s.best.model == "gpt-6-1-sol"
    assert (s.also.tool, s.also.model) == ("claude-code", "claude-opus-5-5")
    assert s.also.q - s.best.q >= S.XV_QUALITY_GAP and s.also.costs["livebench:coding"] > 10 * s.best.costs["livebench:coding"]
    assert _line(S.render(s), "Also consider").startswith("Also consider: claude-code, claude-opus-5-5")
    # Past the gap it is only a pricier model, and the line stays empty.
    gap, S.XV_QUALITY_GAP = S.XV_QUALITY_GAP, s.also.q - s.best.q + 0.01
    try:
        assert _suggest(target="codex").also is None
    finally:
        S.XV_QUALITY_GAP = gap


def test_session_line():
    s = _suggest(session="claude-haiku-5-5")
    assert s.session.model == "claude-haiku-5-5"
    text = S.render(s, "api", "quality")
    assert "Session: claude-code, claude-haiku-5-5 (the model you're using now), effort medium." in text
    same = S.render(_suggest(session="claude-sonnet-5-5"), "api", "quality")
    assert "Session: claude-sonnet-5-5 (the model you're using now) = best value." in same
    assert same.count("claude-sonnet-5-5") == 2
    assert "Session:" not in S.render(_suggest(), "api", "quality")


def test_candidate_without_data_is_listed_not_ranked():
    s = _suggest(target=None, pool="all")
    assert "gpt-6-astra" in s.nodata and "gemini-3-1-pro-preview" in s.nodata
    ranked = {s.best.model, s.value.model}
    assert not ranked & set(s.nodata)
    assert "No data: " in S.render(s, "api", "quality")


def test_livebench_missing_falls_back_to_list_price():
    s = _suggest(lb=LB_MISSING)
    assert s.best.model == "claude-opus-5-5" and s.best.basis == "list price"
    text = S.render(s, "api", "quality")
    assert "list prices, not measured cost" in text
    # Without LiveBench the value option still appears, compared by list price.
    assert s.value.model == "claude-sonnet-5-5" and s.value.basis == "list price"
    assert "Best value: claude-code, claude-sonnet-5-5" in text and "by list price" in text


def test_long_run_slot_switches_main_evidence():
    s = _suggest(slots={"run_length": "long"})
    assert s.best.model == "claude-fable-5-1"
    assert s.best.used[0][0] == "livebench:long_agentic"


def test_flags_keep_only_relevant_ones():
    text = S.render(_suggest(session="claude-haiku-5-5"), "api", "quality")
    flags = [line for line in text.splitlines() if line.startswith("Flags:")][0]
    assert "PRICE-MISMATCH claude-haiku-5-5" in flags
    assert "UNMAPPED" not in flags and "gpt-6-luna" not in flags
    assert "Flags: none" in S.render(_suggest(), "api", "quality")


def test_render_header_data_line_and_budget():
    text = S.render(_suggest(), "api", "quality")
    lines = text.splitlines()
    assert lines[0].startswith("Suggest: build | pool target | snapshot 2026-10-27 (cached) | impact ")
    # Spec, Privacy and attribution: LMArena with its licence and a link, LiveBench, OpenRouter.
    assert lines[-2].startswith("Data: LMArena (CC BY 4.0, https://lmarena.ai/leaderboard), LiveBench 2026-10-25")
    assert "models.dev, OpenRouter" in lines[-2]
    assert "Leaderboards average many tasks; yours may differ." in lines[-2]
    for kw in ({"target": None, "pool": "all", "session": "claude-haiku-5-5"},
               {"session": "claude-haiku-5-5"},
               {"target": None, "pool": "all", "session": "claude-haiku-5-5", "lb": LB_MISSING}):
        out = S.render(_suggest(**kw), "plan", "balanced")
        assert len(out) < S.BUDGET, (len(out), out)


def test_load_snapshot_falls_back_to_bundled():
    fetch.CACHE = Path(tempfile.mkdtemp())
    skill = Path(tempfile.mkdtemp())
    shutil.copy(FIX, skill / "scoreboard.json")

    def down(url):
        raise OSError("offline")
    snap, state, date = S.load_snapshot(skill, False, NOW, get=down)
    assert (state, date) == ("bundled", "2026-10-27")
    assert "claude-opus-5-5" in snap["models"]

    def live(url):
        assert url == S.scoreboard_url()
        return FIX.read_text(encoding="utf-8")
    snap, state, date = S.load_snapshot(skill, False, NOW, get=live)
    assert (state, date) == ("live", "2026-10-27")
    snap, state, _ = S.load_snapshot(skill, False, NOW, get=down)
    assert state == "cached"


def test_load_snapshot_with_nothing_is_missing():
    fetch.CACHE = Path(tempfile.mkdtemp())

    def down(url):
        raise OSError("offline")
    assert S.load_snapshot(Path(tempfile.mkdtemp()), True, NOW, get=down) == (None, "missing", None)


def _toy(models, board=None):
    """A minimal snapshot: lmarena:text only, one row per model."""
    snap = {"boards": {"lmarena:text": board or {"top": 1500, "p30": 1400}}, "flags": [], "models": {}}
    for mid, elo, price in models:
        entry = {"name": mid, "metrics": {"lmarena:text": [{"effort": None, "elo": elo}]}}
        if price:
            entry["price"] = {"in": price[0], "out": price[1]}
        snap["models"][mid] = entry
    return snap


TOY_EV = {"main": {"lmarena:text": 1.0}}


def _toy_choose(snap, ids, pool="all"):
    cands = [S.Candidate(None, m) for m in ids]
    return S.choose(cands, snap, TOY_EV, S.Info("general", pool, "2026-10-27", "cached", LB_MISSING))


def test_unpriced_candidate_does_not_cancel_the_cost_comparison():
    snap = _toy([("a", 1500, (10, 50)), ("b", 1490, (1, 5)), ("c", 1495, None)])
    assert _toy_choose(snap, ["a", "b"]).value.model == "b"
    s = _toy_choose(snap, ["a", "b", "c"])
    assert s.value is not None and s.value.model == "b"
    assert s.best.basis == "list price"
    text = S.render(s, "api", "quality")
    assert "same as best quality" not in text and "list prices, not measured cost" in text


def test_models_below_the_top_30_still_rank_by_their_rating():
    """Every model below a board's 30th place scales to 0; the best is still the highest rated,
    not the first id alphabetically."""
    snap = _toy([("a-low", 1300, (1, 5)), ("z-high", 1350, (1, 5))])
    s = _toy_choose(snap, ["a-low", "z-high"])
    assert s.best.q == 0.0 and s.best.model == "z-high"


def test_value_is_cheapest_model_that_clears_the_win_rate_floor():
    snap = _toy([("a", 1500, (10, 50)), ("b", 1450, (5, 25)), ("c", 1300, (1, 5))])
    s = _toy_choose(snap, ["a", "b", "c"])
    # b: voters prefer a 57% of the time, inside the floor; c: 76%, outside it.
    assert s.value.model == "b"


def test_value_falls_back_to_best_cheaper_model_when_none_clears_the_floor():
    """Decision 2: both options always show unless they are the same model."""
    snap = _toy([("a", 1500, (10, 50)), ("b", 1300, (2, 10)), ("c", 1200, (1, 5))])
    s = _toy_choose(snap, ["a", "b", "c"])
    assert s.value.model == "b"
    text = S.render(s, "api", "quality")
    assert "same as best quality" not in text
    assert "Best value: b. About 1/5 the cost by list price" in text
    assert "voters preferred a about 76% of the time" in text


def test_same_as_best_only_when_nothing_is_cheaper():
    snap = _toy([("a", 1500, (1, 5)), ("b", 1450, (5, 25))])
    s = _toy_choose(snap, ["a", "b"])
    assert s.value is None and "Best value: same as best quality." in S.render(s, "api", "quality")
    # No cost to compare is not the same claim.
    snap = _toy([("a", 1500, None), ("b", 1450, (5, 25))])
    text = S.render(_toy_choose(snap, ["a", "b"]), "api", "quality")
    assert "same as best quality" not in text and "Best value: no cost data to compare with a." in text


def test_value_without_livebench_across_vendors():
    s = _suggest(target=None, pool="all", type_="general", lb=LB_MISSING)
    assert s.value is not None and s.value.basis == "list price"
    assert "same as best quality" not in S.render(s, "api", "quality")


def test_session_model_the_target_cannot_run_is_not_offered():
    s = _suggest(target="codex", session="claude-opus-5-5")
    assert s.session is None
    text = S.render(s, "api", "quality")
    assert "Session: claude-opus-5-5 (the model you're using now) is not offered by codex." in text
    assert "effort" not in _line(text, "Session")
    # With no target named, the session model stays an option.
    assert _suggest(target=None, pool="all", session="claude-haiku-5-5").session.model == "claude-haiku-5-5"


def _line(text, start):
    return next(line for line in text.splitlines() if line.startswith(start))


def test_note_efforts_read_the_effort_block():
    block = (NOTES / "anthropic.md").read_text(encoding="utf-8").split("## Effort")[1].split("\n## ")[0]
    names = {"claude-fable-5-1": "Claude Fable 5.1", "claude-opus-5-5": "Claude Opus 5.5",
             "claude-sonnet-5-5": "Claude Sonnet 5.5", "claude-haiku-5-5": "Claude Haiku 5.5"}
    assert S.note_efforts(block, names) == {"claude-fable-5-1": "high", "claude-opus-5-5": "medium",
                                             "claude-sonnet-5-5": "high", "claude-haiku-5-5": "medium"}
    gem = ("- API: values. Defaults: `medium` on 3.8 and 3.6 Flash, `minimal` on 3.5 Flash-Lite, "
           "`high` on 3.1 Pro and 3 Flash Preview. Per-model levels are in each section.")
    got = S.note_efforts(gem, {"gemini-3-8-flash": "Gemini 3.8 Flash", "gemini-3-6-flash": "Gemini 3.6 Flash",
                               "gemini-3-5-flash-lite": "Gemini 3.5 Flash Lite",
                               "gemini-3-1-pro-preview": "gemini-3-1-pro-preview", "gemini-x": "Gemini X"})
    assert got == {"gemini-3-8-flash": "medium", "gemini-3-6-flash": "medium", "gemini-3-5-flash-lite": "minimal",
                   "gemini-3-1-pro-preview": "high"}
    # A parenthesised default belongs to one model's line, not the family.
    assert S.note_efforts("- K3: values low, high, max (default `max`).", {"kimi-k2-6": "Kimi K2.6"}) == {}


def test_notes_effort_wins_and_openrouter_disagreement_is_flagged():
    snap = S.add_note_efforts(_snap(), REG, NOTES)
    # The fixture's OpenRouter default for Opus is high; the notes say medium.
    assert snap["models"]["claude-opus-5-5"]["efforts"]["notes"] == "medium"
    assert "EFFORT-MISMATCH claude-opus-5-5 notes medium openrouter high" in snap["flags"]
    s = _suggest(snap=snap)
    assert s.best.model == "claude-opus-5-5" and s.best.effort == "medium"
    text = S.render(s, "api", "quality")
    assert "claude-code, claude-opus-5-5, effort medium." in text
    assert "EFFORT-MISMATCH claude-opus-5-5" in _line(text, "Flags")
    # An explicit effort still overrides both.
    assert _suggest(snap=snap, effort="max").best.effort == "max"


def test_unmapped_flags_show_for_the_types_boards_and_are_cut_first():
    s = _suggest(target=None, pool="all", type_="general")
    assert "UNMAPPED lmarena:text MiMo-V2.6-Pro" in s.flags and s.flags[-1].startswith("UNMAPPED")
    # Build's evidence uses no lmarena:text board.
    assert not any(f.startswith("UNMAPPED") for f in _suggest().flags)

    def many(snap):
        snap["flags"] = [f"UNMAPPED lmarena:text Model {i}" for i in range(60)] + snap["flags"]
    s = _suggest(target=None, pool="all", type_="general", snap=_snap(edit=many))
    text = S.render(s, "api", "quality")
    assert len(text) < S.BUDGET and "THIN EVIDENCE general" in _line(text, "Flags") and " more" in text


def test_unmapped_flags_only_for_names_rated_above_every_shown_pick():
    # Opus shows on lmarena:text at 1516.
    def rated(snap):
        snap["flags"] = ["UNMAPPED lmarena:text Old Model @1400", "UNMAPPED lmarena:text New Model @1530",
                         "UNMAPPED lmarena:text Tied Model @1516"] + snap["flags"]
    flags = _suggest(target=None, pool="all", type_="general", snap=_snap(edit=rated)).flags
    assert "UNMAPPED lmarena:text New Model @1530" in flags
    assert not any("Old Model" in f or "Tied Model" in f for f in flags)
    # A flag with no rating (older snapshot) is still shown.
    assert "UNMAPPED lmarena:text MiMo-V2.6-Pro" in flags


def _cut(line, head):
    """(items shown, the +N more count) from a 'No data:' or 'Flags:' line."""
    body, _, more = line[len(head):].rstrip(".").partition(" +")
    return body.split(", "), int(more.split()[0]) if more else 0


def test_render_cuts_long_no_data_and_flag_lists_to_the_budget():
    snap = _toy([("a", 1500, (10, 50)), ("b", 1450, (5, 25))])
    snap["flags"] = [f"PRICE-MISMATCH a source-{i:02d}-disagrees-with-the-majority" for i in range(30)]
    missing = [f"unlisted-model-with-a-long-id-{i:02d}" for i in range(40)]
    s = _toy_choose(snap, ["a", "b"] + missing)
    # 40 of 42 candidates without data also raises THIN EVIDENCE: 31 flags.
    assert len(s.nodata) == 40 and len(s.flags) == 31
    text = S.render(s, "api", "quality")
    assert len(text) < S.BUDGET, len(text)
    nodata, more_nodata = _cut(_line(text, "No data: "), "No data: ")
    flags, more_flags = _cut(_line(text, "Flags: "), "Flags: ")
    # Both lists are cut from the end, and the counts say exactly how many went.
    assert more_nodata and more_flags
    assert nodata == s.nodata[:len(nodata)] and len(nodata) + more_nodata == len(s.nodata)
    assert flags == s.flags[:len(flags)] and len(flags) + more_flags == len(s.flags)
    # The picks themselves are never cut.
    assert "Best quality (Recommended): a." in text and "Best value: b." in text
    # A short list is printed whole.
    short = S.render(_toy_choose(snap, ["a", "b"] + missing[:2]), "api", "quality")
    assert "more" not in _line(short, "No data: ")


def test_thin_evidence_is_said_on_the_line_and_flagged_past_half():
    """Main metric 0.4 of the weight: a model with only it is thin evidence (coverage < THIN)."""
    ev = {"main": {"lmarena:text": 0.4}, "support": {"lmarena:webdev": 0.6}}
    snap = {"boards": {"lmarena:text": {"top": 1500, "p30": 1400}, "lmarena:webdev": {"top": 1500, "p30": 1400}},
            "flags": [], "models": {}}
    for mid, text, web, price in (("a", 1500, 1500, (10, 50)), ("b", 1490, None, (1, 5)),
                                  ("c", None, 1450, (1, 5)), ("d", None, 1440, (1, 5)), ("e", None, 1430, (1, 5))):
        metrics = {k: [{"effort": None, "elo": v}] for k, v in (("lmarena:text", text), ("lmarena:webdev", web)) if v}
        snap["models"][mid] = {"name": mid, "metrics": metrics, "price": {"in": price[0], "out": price[1]}}

    def run(ids):
        return S.choose([S.Candidate(None, m) for m in ids], snap, ev,
                        S.Info("general", "all", "2026-10-27", "cached", LB_MISSING))
    # b has only the main metric: the value line says thin evidence; a's full evidence doesn't.
    s = run(["a", "b", "c", "d"])
    assert s.value.model == "b" and s.thin == ["b"]
    text = S.render(s, "api", "quality")
    assert _line(text, "Best value").endswith("Thin evidence.")
    assert "Thin evidence" not in _line(text, "Best quality")
    # Exactly half the candidates (c, d) lack the main metric: not flagged.
    assert not any(f.startswith("THIN EVIDENCE") for f in s.flags)
    # Three of five is more than half.
    s = run(["a", "b", "c", "d", "e"])
    assert "THIN EVIDENCE general" in s.flags and "THIN EVIDENCE general" in _line(S.render(s), "Flags")
    # A thin best says so on its own line.
    text = S.render(run(["b", "c"]), "api", "quality")
    assert _line(text, "Best quality").startswith("Best quality (Recommended): b.")
    assert _line(text, "Best quality").endswith("LMArena text 1490. Thin evidence.")


def test_value_compares_each_model_on_the_most_specific_basis_it_shares_with_best():
    ev = {"main": {"lmarena:text": 1.0}, "cost_suite": "livebench:coding"}
    snap = _toy([("a", 1500, (10, 50)), ("b", 1495, (2, 10)), ("c", 1495, (1, 5)), ("d", 1498, None),
                 ("f", 1495, (1, 5)), ("g", 1497, (5, 25))])
    m = snap["models"]
    lb = lambda cost: {"score": None, "cost_per_task": cost}
    m["a"]["metrics"].update({"livebench:coding": lb(10.0), "livebench:design": lb(8.0)})
    m["b"]["metrics"]["livebench:design"] = lb(2.0)       # no suite cost: token efficiency
    m["f"]["metrics"].update({"livebench:coding": lb(3.0), "livebench:design": lb(1.0)})

    def run(ids):
        return S.choose([S.Candidate(None, i) for i in ids], snap, ev,
                        S.Info("general", "all", "2026-10-27", "cached", LB_LIVE))
    # Both have the suite cost: compared on it.
    s = run(["a", "f"])
    assert (s.value.model, s.value.basis, s.best.cost) == ("f", "livebench:coding", 10.0)
    assert "per task (LiveBench coding $3.00 vs $10.00)" in _line(S.render(s), "Best value")
    # b has no suite cost: the comparison drops to the LiveBench mean, ahead of list price.
    s = run(["a", "b"])
    assert (s.value.model, s.value.basis, s.best.cost) == ("b", "token-efficiency", 9.0)
    assert "per task (LiveBench mean $2.00 vs $9.00)" in _line(S.render(s), "Best value")
    # c has only a list price: compared, and said to be compared, by list price.
    s = run(["a", "c"])
    assert (s.value.model, s.value.basis) == ("c", "list price")
    text = S.render(s)
    assert "by list price ($2.00 vs $20.00 per M tokens, 3:1 blend)" in _line(text, "Best value")
    assert "list prices, not measured cost" in _line(text, "Data:")
    # d clears the floor but has no cost on any basis: left out, not a reason to drop the value.
    s = run(["a", "d", "b"])
    assert s.value.model == "b" and "same as best quality" not in S.render(s)
    # With g (list price only, half of a's) also clearing it, the cheapest share still wins: b.
    assert run(["a", "d", "g", "b"]).value.model == "b"
    assert "Best value: no cost data to compare with a." in S.render(run(["a", "d"]))


def _media_notes():
    """The frozen family notes plus the real media tools' notes, whose ## sections are their models."""
    d = Path(tempfile.mkdtemp())
    for p in NOTES.glob("*.md"):
        shutil.copy(p, d / p.name)
    for key in ("gpt-image", "nano-banana", "midjourney", "sora", "google-video", "runway"):
        shutil.copy(SKILL / "targets" / f"{key}.md", d / f"{key}.md")
    return d


def _media_snap():
    snap = {"boards": {"lmarena:text_to_image": {"top": 1300, "p30": 1100}}, "flags": [], "models": {},
            "sources": {"lmarena": {"licence": "CC BY 4.0"}}}
    for mid, elo in (("gpt-image-2-5-sunburst", 1300), ("gemini-nano-banana-2-1", 1280)):
        snap["models"][mid] = {"name": mid, "metrics": {"lmarena:text_to_image": [{"effort": None, "elo": elo}]}}
    return snap


def test_media_tools_list_their_own_models_and_make_the_image_pool():
    notes = _media_notes()
    gi = S.candidates("gpt-image", REG, notes, "target", "image")
    assert {c.tool for c in gi} == {"gpt-image"} and ("gpt-image", "gpt-image-2-5-sunburst") in gi
    pool = S.candidates(None, REG, notes, "all", "image")
    assert {c.tool for c in pool} <= set(S.MEDIA_TOOLS["image"]) and pool
    assert not any(c.model.startswith("claude") for c in pool)
    vids = S.candidates(None, REG, notes, "all", "video")
    assert {c.tool for c in vids} <= set(S.MEDIA_TOOLS["video"]) and ("sora", "sora-2") in vids
    ev = S.resolve_evidence(EVIDENCE, "image", {})
    s = S.choose(pool, _media_snap(), ev, S.Info("image", "all", "2026-10-27", "cached", LB_MISSING))
    assert (s.best.tool, s.best.model) == ("gpt-image", "gpt-image-2-5-sunburst")
    text = S.render(s)
    assert "no candidate has data" not in text and "claude" not in text


def test_session_id_strips_context_size_and_matches_exactly():
    """Hosts show 'Opus 5.5 (1M context)'; SKILL's sanitising leaves 'Claude Opus 5.5 1m'. An
    older version is its own model, never the current one."""
    def older(snap):
        snap["models"]["claude-sonnet-5"] = {"name": "Claude Sonnet 5", "metrics": {}}
    snap = _snap(edit=older)
    for name, want in (("Claude Opus 5.5 1m", "claude-opus-5-5"), ("Opus 5.5 1M context", "claude-opus-5-5"),
                       ("Claude Opus 5.5 200k", "claude-opus-5-5"), ("claude-opus-5-5", "claude-opus-5-5"),
                       ("Claude Sonnet 5", "claude-sonnet-5"), ("Claude Sonnet 5.5", "claude-sonnet-5-5"),
                       ("Sonnet 5.5", "claude-sonnet-5-5"), ("Mystery 9", "Mystery 9")):
        assert S.session_id(name, snap) == want, name


def test_no_data_names_each_model_once_across_tools():
    """Pool all for agent types pairs a model with every tool that offers it."""
    s = _suggest(target=None, pool="all", type_="agent")
    assert s.nodata and len(s.nodata) == len(set(s.nodata))


def test_style_words_map_onto_the_image_style_slots():
    """SKILL's sanitising strips underscores, and people say 'photo' or '3D', not the enum."""
    img = EVIDENCE["image"]
    for said, want in (("text rendering", "text_rendering"), ("Text-Rendering", "text_rendering"),
                       ("commercial design", "commercial_design"), ("3D", "3d_modeling"),
                       ("3d modeling", "3d_modeling"), ("photo", "photorealistic"),
                       ("photorealistic", "photorealistic"), ("portrait", "portraits"),
                       ("illustration", "art"), ("logo with text", "text_rendering")):
        got = S.style_slot(said, img)
        assert got == want, (said, got)
        assert S.main_key(S.resolve_evidence(EVIDENCE, "image", {"style": got})) == f"lmarena:text_to_image/{want}"
    assert S.main_key(S.resolve_evidence(EVIDENCE, "image", {"style": S.style_slot("minimal", img)})) \
        == "lmarena:text_to_image"


def test_impact_high_only_at_a_true_3x_cost_ratio():
    """'About 1/3' prints for ratios up to 0.4; the 3x rule is on the ratio itself, so the
    script says which it is and SKILL reads the header."""
    s = _toy_choose(_toy([("a", 1500, (10, 50)), ("b", 1490, (4, 18.4))]), ["a", "b"])
    assert "About 1/3 the cost" in _line(S.render(s), "Best value")   # 0.38 of a's cost
    assert s.impact == "low" and S.render(s).splitlines()[0].endswith("| impact low")
    s = _toy_choose(_toy([("a", 1500, (10, 50)), ("b", 1490, (3, 15))]), ["a", "b"])   # 0.30
    assert s.impact == "high" and S.render(s).splitlines()[0].endswith("| impact high")
    assert _toy_choose(_toy([("a", 1500, None)]), ["a"]).impact == "low"


def test_impact_high_when_the_picks_lead_is_material():
    """Design: high-impact when costs span 3x or the pick's lead is material. A near-equal or
    merely non-tied value option is not a material lead; the person's own model falling below
    the value floor, or another vendor clearly better, is."""
    snap = _toy([("a", 1500, (10, 50)), ("b", 1450, (8, 40)), ("c", 1300, (9, 45))])
    plain = S.choose([S.Candidate(None, m) for m in "ab"], snap, TOY_EV,
                     S.Info("general", "all", "2026-10-27", "cached", LB_MISSING))
    assert "voters preferred a about 57%" in S.render(plain) and plain.impact == "low"
    with_session = lambda m: S.choose([S.Candidate(None, x) for x in "ab"], snap, TOY_EV,
                                      S.Info("general", "all", "2026-10-27", "cached", LB_MISSING), session=m)
    assert with_session("c").impact == "high"     # voters prefer a over c 76% of the time
    assert with_session("b").impact == "low"      # the session model is the value option
    same = _toy_choose(_toy([("a", 1500, (1, 5)), ("b", 1450, (5, 25))]), ["a", "b"])
    assert same.value is None and same.impact == "low"
    snap = _toy([("a", 1500, (10, 50)), ("b", 1490, (8, 40)), ("x", 1600, (10, 50))], {"top": 1600, "p30": 1400})
    s = S.choose([S.Candidate("t", "a"), S.Candidate("t", "b")], snap, TOY_EV,
                 S.Info("general", "target", "2026-10-27", "cached", LB_MISSING, "t"),
                 others=[S.Candidate("u", "x")])
    assert s.also.model == "x" and s.impact == "high"
