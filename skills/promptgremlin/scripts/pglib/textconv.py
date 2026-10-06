"""Turn fetched text into markdown-ish text, according to the source's format."""
import json
import re
from html.parser import HTMLParser

MARKDOWN_FORMATS = {"md", "md.txt", "text", "github-api"}
FORMATS = MARKDOWN_FORMATS | {"json-helpcenter", "html"}

# Mintlify/GitBook pages embed JSX components; the prose between them is what we want.
JSX_LINE = re.compile(r"^\s*</?[A-Z][A-Za-z0-9.]*\b[^>]*/?>\s*$")
EXPORT_START = re.compile(r"^export\s+const\s")
OPENERS = ("{", "(", "=", "[", "=>")


def strip_jsx(text):
    out, skipping = [], False
    for line in text.splitlines():
        if skipping:
            if line.rstrip() in ("};", "}", ");", ")", "];", "]"):
                skipping = False
            continue
        if EXPORT_START.match(line):
            skipping = line.rstrip().endswith(OPENERS)  # only an open construct spans lines
            continue
        if JSX_LINE.match(line):
            continue
        out.append(line)
    return "\n".join(out)


class _ToMarkdown(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "nav", "footer"}
    BLOCK = {"p", "div", "section", "article", "br", "tr", "table", "ul", "ol", "pre", "blockquote"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif self.skip:
            return
        elif tag in ("h1", "h2", "h3", "h4"):
            self.out.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag == "li":
            self.out.append("\n- ")
        elif tag in self.BLOCK:
            self.out.append("\n\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
        elif not self.skip and (tag in ("h1", "h2", "h3", "h4") or tag in self.BLOCK):
            self.out.append("\n\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data if data.strip() else " ")


def html_to_md(raw):
    p = _ToMarkdown()
    p.feed(raw)
    p.close()
    lines = []
    for line in "".join(p.out).splitlines():
        line = re.sub(r"[ \t ]+", " ", line).strip()
        lines.append(re.sub(r"^(#{1,4}) +", r"\1 ", line))
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


# Anti-bot interstitials (served to CI runners) look like pages; treating them as docs fakes a DRIFT.
BOT_MARKERS = ("cf-chl", "attention required! | cloudflare")  # technical, matched on the raw body
# Phrases also appear in real pages (llama.com embeds a hidden SSO "confirm your identity" dialog), so they are
# matched on the converted text (not scripts/attributes) and only when that text is short, as challenge pages are.
BOT_PHRASES = (
    "please confirm your identity", "verify you are human", "checking your browser",
    "just a moment...", "enable javascript and cookies to continue",
)
BOT_PHRASE_MAX_CHARS = 2000


def _check_bot_challenge(raw, converted):
    low = converted.lower()
    if any(m in raw.lower() for m in BOT_MARKERS) or (
            len(converted) < BOT_PHRASE_MAX_CHARS and any(m in low for m in BOT_PHRASES)):
        raise ValueError("bot challenge page")


def to_text(raw, fmt):
    if fmt not in FORMATS:
        raise ValueError(f"unknown source format: {fmt}")
    if fmt in MARKDOWN_FORMATS:
        if raw.lstrip()[:20].lower().startswith(("<!doctype", "<html")):
            raise ValueError("got an HTML page where markdown was expected")
        return strip_jsx(raw)
    if fmt == "json-helpcenter":
        art = json.loads(raw)["article"]
        out = f"# {art.get('title', '')}\n\n{html_to_md(art.get('body', ''))}"
    else:
        out = html_to_md(raw)
    _check_bot_challenge(raw, out)
    return out
