import json
import tempfile
from pathlib import Path

import guidance


def _skill_dir(reg):
    d = Path(tempfile.mkdtemp())
    (d / "targets").mkdir()
    (d / "sources.json").write_text(json.dumps(reg))
    return d


def test_unknown_target_exits_2():
    guidance.SKILL_DIR = _skill_dir({})
    assert guidance.main(["--target", "nope", "--offline"]) == 2


def test_missing_notes_exits_2():
    guidance.SKILL_DIR = _skill_dir({"y": {"kind": "tool", "sources": {"a": {"format": "none"}}}})
    assert guidance.main(["--target", "y", "--offline"]) == 2


def test_offline_run_exits_0():
    d = _skill_dir({"y": {"kind": "tool", "sources": {"a": {"format": "none"}}}})
    (d / "targets" / "y.md").write_text("---\nfamily: y\nkind: tool\nlast_verified: 2026-09-30\n"
                                         "sources: []\n---\n## All models\n- hi\n")
    guidance.SKILL_DIR = d
    assert guidance.main(["--target", "y", "--offline"]) == 0


def test_refresh_commit_without_notes_exits_2_before_fetch():
    """--refresh X --commit with no notes file should exit 2 without fetching."""
    d = _skill_dir({"y": {"kind": "tool", "sources": {"a": {"format": "none"}}}})
    # No notes file for y
    guidance.SKILL_DIR = d
    assert guidance.main(["--refresh", "y", "--commit", "--offline"]) == 2
