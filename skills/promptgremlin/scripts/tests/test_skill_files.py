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


def _section(text, heading):
    parts = re.split(r"^## ", text, flags=re.M)
    for part in parts:
        if part.startswith(heading):
            return part
    raise AssertionError(f"missing section {heading}")


def _slot(slots, name):
    match = re.search(
        rf"\*\*{re.escape(name)}\*\*.*?(?=\n\d+\. \*\*|\Z)", slots, re.S)
    assert match, name
    return match.group(0)


def test_build_clone_request_suggests_full_feature_set_and_solid_finish():
    """A clone or 'identical to X' request suggests the whole feature set and a solid v1."""
    text = (SKILL / "types" / "build.md").read_text()
    slots = _section(text, "Slots")
    features = _slot(slots, "v1 features").lower()
    assert "clone" in features
    assert "identical" in features
    assert "full feature set" in features
    # Thin wording still gets a small suggestion, so scope scales with ambition.
    assert "2–3" in features or "2-3" in features
    speed = _slot(slots, "speed").lower()
    assert "solid v1" in speed
    assert "clone" in speed and "identical" in speed


def test_build_long_run_writes_post_checklist_stretch_phase():
    """A long-run answer is a run-length slot that adds a stretch phase after the checklist."""
    text = (SKILL / "types" / "build.md").read_text()
    slots = _section(text, "Slots")
    run = _slot(slots, "run length").lower()
    assert "budget" in run
    assert "long run" in run
    skeleton = _section(text, "Prompt skeleton").lower()
    assert "stretch phase" in skeleton
    assert "after the checklist" in skeleton
    guidance = _section(text, "Type guidance").lower()
    assert "stretch phase" in guidance
    assert "long run" in guidance


def test_writer_keeps_unattended_builds_runnable_and_claude_end_steps():
    """Unattended builds stay runnable per milestone; CLAUDE.md overrides keep end steps."""
    body = " ".join((SKILL / "writer.md").read_text().split())
    assert "running slice" in body and "before any docs" in body
    assert "After each milestone the app still runs" in body
    assert "PROGRESS.md" in body
    assert "per-milestone runnable and handoff rule" in body
    assert "including in the done line" in body
    assert "overrides part of the person's CLAUDE.md" in body
    assert "end-of-work steps" in body
    assert "writer requirement in section 3" in body
    assert "Writer requirements from section 3 stay" in body
    assert "A writer requirement from section 3 stays" in body
    assert "PROGRESS.md is the" in body and "handoff file for an unattended build" in body


def test_writer_flags_found_and_added_defaults_for_veto():
    """TOOL-68: no first person for things the person didn't say; a veto list for found or added items."""
    body = " ".join((SKILL / "writer.md").read_text().split())
    assert "first person" in body and "only for what the person said" in body
    assert "**found**" in body and "**added**" in body
    assert "Defaults I added — veto any" in body
    assert "Omit the list only when every instruction was confirmed" in body
    port = (SKILL / "modes" / "port.md").read_text()
    assert "Defaults I added — veto any" in port


def test_agent_targets_get_a_run_setup_question_and_where_to_run_line():
    """TOOL-67: run setup is asked before writing for agent tools; delivery ends with where to run."""
    skill = " ".join((SKILL / "SKILL.md").read_text().split())
    assert "**Run setup**" in skill and "claude-code, codex" in skill
    assert "asked in the first round" in skill
    assert "Never default silently to a flagship" in skill
    assert "Run: <surface> | <model or unset> | <effort>" in skill
    writer = " ".join((SKILL / "writer.md").read_text().split())
    assert "pass it as `--model`" in writer
    assert "**Where to run**" in writer and "never do the task in this conversation" in writer


def test_relay_keeps_fences_through_the_hand_back_frame():
    """The writer's reply is indented in a hand-back frame; the relay must keep its fence lines."""
    body = " ".join((SKILL / "SKILL.md").read_text().split())
    assert "hand-back frame with every line indented" in body
    assert "keep every ``` fence line, at the left margin" in body
