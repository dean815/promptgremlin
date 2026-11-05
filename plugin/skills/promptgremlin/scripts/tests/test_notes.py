import datetime as dt

from pglib import notes

NOTE = ("---\nfamily: anthropic\nkind: family\nlast_verified: 2026-06-01\n"
        "sources: [best-practices, effort]\n---\n## All models\n- rule one\n\n"
        "## Effort\n- /effort\n\n## claude-opus-5-5\n- opus delta\n\n## claude-sonnet-4-5\n- old\n")


def test_parse_meta_and_blocks():
    n = notes.parse(NOTE)
    assert n.meta["family"] == "anthropic"
    assert n.meta["sources"] == ["best-practices", "effort"]
    assert list(n.blocks) == ["All models", "Effort", "claude-opus-5-5", "claude-sonnet-4-5"]
    assert n.blocks["claude-opus-5-5"] == "- opus delta"


def test_model_ids_exclude_reserved_blocks():
    assert notes.model_ids(notes.parse(NOTE)) == ["claude-opus-5-5", "claude-sonnet-4-5"]


def test_is_stale_after_90_days():
    n = notes.parse(NOTE)
    assert notes.is_stale(n, dt.date(2026, 10, 1))
    assert not notes.is_stale(n, dt.date(2026, 7, 1))


def test_edit_and_roundtrip():
    n = notes.set_last_verified(notes.parse(NOTE), "2026-10-01")
    n, removed = notes.remove_blocks(n, ["claude-sonnet-4-5"])
    again = notes.parse(notes.render(n))
    assert again.meta["last_verified"] == "2026-10-01"
    assert again.meta["sources"] == ["best-practices", "effort"]
    assert "claude-sonnet-4-5" not in again.blocks
    assert removed == {"claude-sonnet-4-5": "- old"}
