"""bench.py's Model-block checks, on replies written by hand. No network, no claude CLI."""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("bench", Path(__file__).resolve().parents[1] / "bench.py")
B = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(B)

SEEN = """Suggest: change-code | pool target | snapshot 2026-11-02 (bundled) | impact high
Best quality (Recommended): claude-code, claude-opus-5-5, effort medium. LMArena text coding 1520 (Oct 28), LiveBench coding 96.3.
Best value: claude-code, claude-sonnet-5-5, effort high. About 20% cheaper per task (LiveBench coding $4.02 vs $5.03); voters preferred Claude Opus 5.5 about 58% of the time.
Also consider: codex, gpt-6-1-sol, effort medium. About 1/10 the cost per task (LiveBench coding $0.48 vs $5.03); voters preferred Claude Opus 5.5 about 58% of the time.
Data: LMArena (CC BY 4.0, https://lmarena.ai/leaderboard), LiveBench 2026-10-25 (stale), models.dev, OpenRouter; snapshot 2026-11-02. Leaderboards average many tasks; yours may differ.
Flags: LIVEBENCH-STALE"""
OPTIONS = SEEN.splitlines()[1:5]


def _reply(block_lines, head="**Model:**"):
    return "\n".join(["```", "Fix the slow CSV export." * 5, "```", "Effort: medium", "", head,
                      *block_lines, "", "Where to run: Claude Code CLI, claude-opus-5-5, /effort medium."])


def test_model_block_reads_a_verbatim_block():
    for head in ("**Model:**", "Model:", "## Model"):
        block = B.model_block(_reply(OPTIONS, head))
        assert block == "\n".join(OPTIONS), head
    assert B.model_block("no block here") is None


def test_bold_option_labels_are_a_reformatted_block_not_a_missing_one():
    bold = ["**Best quality (Recommended):** " + OPTIONS[0].split(": ", 1)[1], *OPTIONS[1:]]
    block = B.model_block(_reply(bold))
    assert block and "Best value" in block and "Data:" in block
    assert B.verbatim(block, SEEN) is False
    assert B.verbatim(B.model_block(_reply(OPTIONS)), SEEN) is True


def test_unsourced_catches_rounded_truncated_and_reworded_numbers():
    assert B.unsourced("\n".join(OPTIONS), SEEN) == []
    bad = "LiveBench coding 96. 10x cheaper ($5 vs $0.48), about 5x, 10% cheaper, 58% of the time"
    assert B.unsourced(bad, SEEN) == sorted({"96", "10x", "$5", "5x", "10%"})
    # Digits inside model ids and dates are not numbers the writer stated.
    assert B.unsourced("claude-opus-5-5 and gpt-6-1-sol, LiveBench 2026-10-25", SEEN) == []


def test_one_round_is_checked_for_quick_only():
    rows = B.model_rows({"t": {"quick": [{"applies": True, "rounds": 1}], "deep": [{"applies": True, "rounds": 3}]}})
    assert rows["t"]["quick"]["one_round"] == "1/1" and rows["t"]["deep"]["one_round"] == "-"


def test_relay_measures_lines_the_skill_dropped():
    writer = _reply(OPTIONS)
    assert B.relayed(writer, writer) == 1.0
    # The skill's own short paraphrase keeps the prompt but loses the block.
    short = "\n".join(["```", "Fix the slow CSV export." * 5, "```", "Run this in Claude Code on Opus 5.5."])
    assert B.relayed(writer, short) < B.RELAY_OK
    assert B.relayed(None, short) is None
