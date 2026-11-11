"""Split markdown by heading, tidy it, and detect changes against stored fingerprints."""
import hashlib
import re
import unicodedata

HEADING = re.compile(r"^(#{1,3}) (.+?)\s*$")
JSX = re.compile(r"^\s*</?(Accordion|AccordionGroup|Tip|Note|Warning|Info|CardGroup|Card|"
                 r"Tabs|Tab|Frame|Steps|Step)\b[^>]*>\s*$")
CODE_FENCE_MAX_LINES = 25
INLINE_TAG = re.compile(r"<[^>]*>")


FENCE = re.compile(r"(`{3,})(.*)")


def fence_step(line, open_ticks):
    """Track a code fence across lines: the opener's backtick count while inside one, else None.

    A fence closes on a bare run of at least as many backticks as opened it. A fence line with an
    info string (```python) met while one is open, and at least as long, starts a new fence: a
    vendor page with one stray ``` would otherwise read everything after it as code.
    """
    m = FENCE.match(line.strip())
    if not m:
        return open_ticks
    ticks, info = len(m.group(1)), m.group(2).strip()
    if open_ticks is None:
        return ticks
    if ticks < open_ticks:
        return open_ticks
    return ticks if info else None


def _invisible(text):
    """Drop format characters (zero-width spaces and joiners, bidi controls, BOM): vendor pages
    put U+200B in headings, and the keys stored in sources.json must not carry them."""
    return "".join(ch for ch in text if unicodedata.category(ch) != "Cf")


def _title(raw):
    """Heading text without inline HTML such as <span id="x"/> or invisible characters; the raw
    text if nothing is left."""
    raw = _invisible(raw)
    return INLINE_TAG.sub("", raw).strip() or raw.strip()


def strip_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


def sections(text):
    """[(level, title, body)] for every H1-H3; body stops at the next heading of any level."""
    out, level, title, buf = [], None, None, []
    fence = None
    for line in strip_frontmatter(text).splitlines():
        was, fence = fence, fence_step(line, fence)
        if was is not None or fence is not None:
            buf.append(line)
            continue
        m = HEADING.match(line)
        if m:
            if title is not None:
                out.append((level, title, "\n".join(buf).strip()))
            level, title, buf = len(m.group(1)), _title(m.group(2)), []
        else:
            buf.append(line)
    if title is not None:
        out.append((level, title, "\n".join(buf).strip()))
    return out


def h2_blocks(text):
    """{H2 title: everything until the next H2, H3 children included}."""
    out, title, buf = {}, None, []
    fence = None
    for line in strip_frontmatter(text).splitlines():
        was, fence = fence, fence_step(line, fence)
        if was is not None or fence is not None:
            if title is not None:
                buf.append(line)
            continue
        m = HEADING.match(line)
        if m and len(m.group(1)) == 2:
            if title is not None:
                out.setdefault(title, "\n".join(buf).strip())
            title, buf = _title(m.group(2)), []
        elif title is not None:
            buf.append(line)
    if title is not None:
        out.setdefault(title, "\n".join(buf).strip())
    return out


def clean(body):
    """Drop JSX wrapper lines (content stays) and collapse very long code fences."""
    out, fence, fence_buf = [], False, []
    for line in body.splitlines():
        if line.strip().startswith("```"):
            if not fence:
                fence, fence_buf = True, [line]
            else:
                fence_buf.append(line)
                if len(fence_buf) > CODE_FENCE_MAX_LINES + 2:
                    out.extend(fence_buf[:11])
                    out.append(f"... [{len(fence_buf) - 12} lines omitted]")
                    out.append(fence_buf[-1])
                else:
                    out.extend(fence_buf)
                fence = False
            continue
        if fence:
            fence_buf.append(line)
        elif not JSX.match(line):
            out.append(line)
    if fence:
        out.extend(fence_buf)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def cap(text, limit):
    if len(text) <= limit:
        return text
    cut = text[:limit]
    nl = cut.rfind("\n\n")
    if nl > limit // 2:
        cut = cut[:nl]
    return cut.rstrip() + f"\n\n... [section truncated at {limit} chars; full text at source]"


# Pages like Google's support footer embed a per-request random ID (12+ digits); it is not content.
LONG_DIGITS = re.compile(r"\b\d{12,}\b")


def fingerprint(body):
    norm = LONG_DIGITS.sub("#", " ".join(body.split()))
    return "sha256:" + hashlib.sha256(norm.encode()).hexdigest()[:16]


def watched(text, watch):
    """Return ({title: body}, missing_titles, all H2/H3 titles) for a watch spec.

    watch == ["*"]  -> the whole page as one section
    watch == ["##"] -> every H2 block (whole page if the page has no H2)
    otherwise       -> the named H1-H3 sections
    """
    secs = sections(text)
    heads = [t for lvl, t, _ in secs if lvl in (2, 3)]
    if watch == ["*"]:
        return {"*": strip_frontmatter(text)}, [], heads
    if watch == ["##"]:
        return (h2_blocks(text) or {"*": strip_frontmatter(text)}), [], heads
    by_title = {}
    for _, t, b in secs:
        by_title.setdefault(t, b)
    found = {t: by_title[t] for t in watch if t in by_title}
    return found, [t for t in watch if t not in by_title], heads


LABEL_KEEP = set(" .,:;()&'/+-_?!*")  # * is the whole-page key
LABEL_CAP = 60


def label(title):
    """A page heading as it may print outside the vendor-text fence: letters, digits and plain
    punctuation only, at most LABEL_CAP characters. Headings are page text, so they stay short."""
    kept = "".join(c if c.isalnum() or c in LABEL_KEEP else " " for c in _invisible(title))
    kept = " ".join(kept.split())
    return kept if len(kept) <= LABEL_CAP else kept[:LABEL_CAP - 3].rstrip() + "..."


def drift(source_key, text, watch, fp):
    found, missing, heads = watched(text, watch)
    # Details name headings and print as flags, so each heading goes through label().
    out = [("missing", f"{source_key}#{label(t)}", "") for t in missing]
    stored = fp.get("sections", {})
    # a section that was fingerprinted but is gone from the page (named watches are in `missing`)
    out += [("missing", f"{source_key}#{label(t)}", "") for t in stored
            if t not in found and t not in missing]
    for t, b in found.items():
        if stored.get(t) != fingerprint(b):
            out.append(("changed", f"{source_key}#{label(t)}", b))
    known = set(fp.get("headings", []))
    if known:
        new = [h for h in heads if h not in known]
        if new:
            out.append(("new", f"{source_key}: " + ", ".join(label(h) for h in new[:8]), ""))
    return out
