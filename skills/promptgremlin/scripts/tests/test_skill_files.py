import re
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2]


def _frontmatter(text):
    return text.split("\n---", 1)[0]


def test_description_short_and_names_no_tools():
    fm = _frontmatter((SKILL / "SKILL.md").read_text())
    desc = re.search(r"^description: (.+)$", fm, re.M).group(1)
    assert len(desc.split()) <= 110, len(desc.split())   # ~150 tokens
    for name in ("Midjourney", "ChatGPT", "Cursor", "Gemini", "Grok", "Claude Code"):
        assert name not in desc, name
    # v3 interviews in the main conversation, so the skill must not fork.
    assert not re.search(r"^context: fork$", fm, re.M)


def test_skill_mentions_every_flag_and_mode_file():
    body = (SKILL / "SKILL.md").read_text() + (SKILL / "writer.md").read_text()
    for needle in ("NEW MODEL", "RETIRED", "UNKNOWN MODEL", "DRIFT", "STALE", "FETCH-FAIL",
                   "modes/port.md", "modes/autopsy.md", "effort.md", "Embedded instructions",
                   "~/.config/promptgremlin/config.json"):
        assert needle in body, needle


def load_banned(path):
    """Parse an optional local list of terms to keep out of published files.

    Lines: blank and # comments are skipped, /regex/ lines are regexes, anything else is a
    literal. Returns a list of (term, is_regex). A missing file gives [].
    """
    path = Path(path)
    if not path.is_file():
        return []
    out = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if len(line) > 2 and line.startswith("/") and line.endswith("/"):
            out.append((line[1:-1], True))
        else:
            out.append((line, False))
    return out


def find_banned(text, banned):
    return [t for t, rx in banned if (re.search(t, text) if rx else t in text)]


def test_banned_file_parsing(tmp_path=None):
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "banned.txt"
        f.write_text("# comment\n\nZorblax\n/\\bQuux\\b/\n")
        banned = load_banned(f)
        assert banned == [("Zorblax", False), (r"\bQuux\b", True)]
        assert find_banned("a Zorblax here", banned) == ["Zorblax"]
        assert find_banned("zorblax", banned) == []
        assert find_banned("the Quux!", banned) == [r"\bQuux\b"]
        assert find_banned("Quuxes", banned) == []
    assert load_banned(Path("/nonexistent/banned.txt")) == []


def test_no_banned_terms_in_published_files():
    """Skip unless an optional local list exists at ~/.config/promptgremlin/banned.txt."""
    banned = load_banned(Path.home() / ".config" / "promptgremlin" / "banned.txt")
    if not banned:
        return
    for p in [SKILL / "SKILL.md", SKILL / "effort.md", *(SKILL / "modes").glob("*.md"),
              *(SKILL / "targets").glob("*.md")]:
        hits = find_banned(p.read_text(), banned)
        assert not hits, (p, hits)


def test_skill_has_no_heredoc_and_uses_a_temp_file_for_the_clipboard():
    body = (SKILL / "SKILL.md").read_text() + (SKILL / "writer.md").read_text()
    assert "<<'PROMPT'" not in body and "<<PROMPT" not in body and "<<'EOF'" not in body
    assert "mktemp -d" in body and "prompt.txt" in body
    assert "< '<dir>/prompt.txt' && rm -rf '<dir>'" in body
    assert "$tmpfile" not in body


def test_skill_quotes_shell_arguments_and_sanitises_them():
    body = (SKILL / "SKILL.md").read_text() + (SKILL / "writer.md").read_text()
    assert "python3 '<skill dir>/scripts/guidance.py'" in body
    assert "--target '<target>'" in body and "--model '<model>'" in body
    assert '--target "' not in body
    assert "letters, digits, dot, dash, space" in body


def test_skill_treats_fetched_guidance_as_reference_not_instructions():
    body = (SKILL / "SKILL.md").read_text() + (SKILL / "writer.md").read_text()
    assert "vendor-text" in body
    assert "never instructions" in body and "Embedded instructions" in body


def test_skill_says_only_changed_section_text_is_fenced():
    body = (SKILL / "SKILL.md").read_text() + (SKILL / "writer.md").read_text()
    assert "the notes, and the text under" not in body
    assert "only the text under" in body
