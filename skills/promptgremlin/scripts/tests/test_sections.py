from pglib import sections as s

DOC = ("---\nt: x\n---\n## Intro\nhi\n### Be clear\nSay it.\n"
       "### Overeagerness\nDo less.\n## Other\nz\n")


def test_sections_split_on_h1_to_h3():
    assert [t for _, t, _ in s.sections(DOC)] == ["Intro", "Be clear", "Overeagerness", "Other"]


def test_h2_blocks_include_children():
    blocks = s.h2_blocks(DOC)
    assert list(blocks) == ["Intro", "Other"]
    assert "### Be clear" in blocks["Intro"] and "Do less." in blocks["Intro"]


def test_fingerprint_ignores_whitespace_only():
    assert s.fingerprint("a  b\n c") == s.fingerprint("a b c")
    assert s.fingerprint("a") != s.fingerprint("b")


def test_watched_modes():
    found, missing, heads = s.watched(DOC, ["*"])
    assert list(found) == ["*"] and missing == []
    found, _, _ = s.watched(DOC, ["##"])
    assert list(found) == ["Intro", "Other"]
    found, missing, heads = s.watched(DOC, ["Be clear", "Gone"])
    assert found == {"Be clear": "Say it."} and missing == ["Gone"]
    assert heads == ["Intro", "Be clear", "Overeagerness", "Other"]


def test_watched_h2_mode_falls_back_to_whole_page():
    found, _, _ = s.watched("# Only a title\ntext", ["##"])
    assert list(found) == ["*"]


def test_drift_unfingerprinted_counts_as_changed():
    assert s.drift("bp", DOC, ["Be clear"], {}) == [("changed", "bp#Be clear", "Say it.")]


def test_drift_clean_when_hashes_match():
    fp = {"sections": {"Be clear": s.fingerprint("Say it.")},
          "headings": ["Intro", "Be clear", "Overeagerness", "Other"]}
    assert s.drift("bp", DOC, ["Be clear"], fp) == []


def test_drift_missing_and_new_headings():
    fp = {"sections": {}, "headings": ["Intro", "Be clear", "Other"]}
    d = s.drift("bp", DOC, ["Gone"], fp)
    assert ("missing", "bp#Gone", "") in d
    assert ("new", "bp: Overeagerness", "") in d


def test_clean_collapses_long_fences_and_jsx():
    body = "keep\n<Accordion title='x'>\ninner\n</Accordion>\n```text\n" + \
           "\n".join(f"line {i}" for i in range(40)) + "\n```"
    out = s.clean(body)
    assert "inner" in out and "<Accordion" not in out
    assert "lines omitted]" in out and "line 39" not in out


def test_cap_truncates_on_paragraph():
    out = s.cap("para one\n\n" + "x" * 3000 + "\n\npara three", 1800)
    assert out.endswith("full text at source]") and len(out) < 2000


def test_sections_ignores_headings_in_code_fences():
    doc_with_fence = ("## Real H2\nIntro text\n```bash\n# not a heading\n## also not\n```\n"
                      "Body after fence\n")
    titles = [t for _, t, _ in s.sections(doc_with_fence)]
    assert titles == ["Real H2"]
    blocks = s.h2_blocks(doc_with_fence)
    assert list(blocks) == ["Real H2"]
    assert "# not a heading" in blocks["Real H2"] and "## also not" in blocks["Real H2"]


def test_watched_star_mode_excludes_frontmatter():
    doc_with_fm = "---\nlastmod: 2024-01-01\n---\n## Section\nContent here\n"
    found, _, _ = s.watched(doc_with_fm, ["*"])
    assert list(found) == ["*"]
    assert "---" not in found["*"] and "lastmod" not in found["*"]
    assert "## Section" in found["*"] and "Content here" in found["*"]


def test_drift_flags_fingerprinted_section_that_vanished():
    two = "## A\none\n## B\ntwo\n"
    found, _, heads = s.watched(two, ["##"])
    fp = {"sections": {t: s.fingerprint(b) for t, b in found.items()}, "headings": heads}
    assert s.drift("k", two, ["##"], fp) == []
    out = s.drift("k", "## A\none\n", ["##"], fp)
    assert ("missing", "k#B", "") in out
    # named watch: reported once, not duplicated
    named = {"sections": {"A": s.fingerprint("one"), "B": s.fingerprint("two")}}
    out = s.drift("k", "## A\none\n", ["A", "B"], named)
    assert out.count(("missing", "k#B", "")) == 1


def test_heading_inline_html_is_stripped_from_titles():
    doc = '## Tips <span id="x"/>\nbody\n### Sub <a name="y"></a>\nmore\n'
    assert [t for _, t, _ in s.sections(doc)] == ["Tips", "Sub"]
    assert list(s.h2_blocks(doc)) == ["Tips"]


def test_fingerprint_ignores_long_digit_runs_but_not_short_numbers():
    a = s.fingerprint("tips\n\n5348562860605714383\n\ntrue")
    b = s.fingerprint("tips\n\n11940056044397967260\n\ntrue")
    assert a == b
    assert s.fingerprint("limit 10 seconds") != s.fingerprint("limit 20 seconds")
