import json
from pglib import textconv as t


def test_strip_jsx_drops_wrappers_and_exports():
    src = ("# Title\nexport const Embed = () => {\n  return 1;\n};\n"
           "<Tip>\nkeep me\n</Tip>\nexport const X = 1;\nend")
    out = t.strip_jsx(src)
    assert "keep me" in out and "end" in out and "# Title" in out
    assert "export" not in out and "<Tip>" not in out and "return 1" not in out


def test_html_to_md_headings_lists_and_skips_scripts():
    src = ("<html><head><style>x{}</style></head><body><nav>menu</nav>"
           "<h2>Prompt tips</h2><p>Be <b>specific</b>.</p><ul><li>one</li><li>two</li></ul>"
           "<script>bad()</script></body></html>")
    out = t.html_to_md(src)
    assert "## Prompt tips" in out
    assert "Be specific." in out
    assert "- one" in out and "- two" in out
    assert "bad()" not in out and "menu" not in out and "x{}" not in out


def test_helpcenter_json_uses_title_and_body():
    raw = '{"article": {"title": "Prompt Basics", "body": "<h2>Order</h2><p>Subject first.</p>"}}'
    out = t.to_text(raw, "json-helpcenter")
    assert out.startswith("# Prompt Basics")
    assert "## Order" in out and "Subject first." in out


def test_markdown_format_rejects_html_shell():
    try:
        t.to_text("<!DOCTYPE html><html>app</html>", "md")
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_unknown_format_raises():
    try:
        t.to_text("x", "pdf")
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_strip_jsx_one_line_export_without_semicolon_keeps_rest():
    out = t.strip_jsx("# T\nexport const X = 1\nreal prose\n## Next\nmore")
    assert "real prose" in out and "## Next" in out and "more" in out and "export" not in out


def test_strip_jsx_multiline_export_still_skipped():
    out = t.strip_jsx("export const A = {\n  a: 1,\n}\nkept\nexport const B = (\n  <x/>\n);\nalso")
    assert "kept" in out and "also" in out and "a: 1" not in out and "<x/>" not in out


def _raises(raw, fmt, msg="bot challenge page"):
    try:
        t.to_text(raw, fmt)
    except ValueError as e:
        assert msg in str(e)
        return
    raise AssertionError("expected ValueError")


def test_bot_challenge_html_raises():
    _raises("<html><body><h1>Please confirm your identity</h1><p>Checking...</p></body></html>", "html")
    _raises("<html><title>Just a moment...</title></html>", "html")
    _raises("<html><script src='/cdn-cgi/x?cf-chl-bypass=1'></script></html>", "html")


def test_bot_challenge_helpcenter_raises():
    raw = '{"article": {"title": "T", "body": "<p>Verify you are human to continue</p>"}}'
    _raises(raw, "json-helpcenter")


def test_captcha_mention_in_long_real_doc_is_fine():
    body = "<h1>Guide</h1>" + "<p>Real documentation sentence about prompts.</p>" * 120
    body += "<p>Some sites show a CAPTCHA to bots.</p>"
    out = t.to_text(f"<html><body>{body}</body></html>", "html")
    assert "CAPTCHA" in out


def test_phrase_on_short_page_raises():
    _raises("<html><body><div>Please verify you are human</div></body></html>", "html")


def test_identity_phrase_in_long_real_page_is_fine():
    body = "<h2>Please confirm your identity</h2>" + "<p>Real documentation sentence.</p>" * 120
    assert "Real documentation" in t.to_text(f"<html><body>{body}</body></html>", "html")


def test_challenge_platform_script_alone_is_fine():
    body = "<h1>Guide</h1><p>Short real doc.</p><script src='/cdn-cgi/challenge-platform/scripts/jsd/main.js'></script>"
    assert "Short real doc." in t.to_text(f"<html><body>{body}</body></html>", "html")


def test_short_article_mentioning_captcha_in_prose_is_fine():
    raw = '{"article": {"title": "Login", "body": "<p>If a CAPTCHA appears, solve it and continue.</p>"}}'
    assert "CAPTCHA" in t.to_text(raw, "json-helpcenter")


def test_recaptcha_in_script_attribute_of_long_page_is_fine():
    body = "<div class='g-recaptcha'></div><script>grecaptcha.ready()</script>" + "<p>Real documentation sentence.</p>" * 120
    assert "Real documentation" in t.to_text(f"<html><body>{body}</body></html>", "html")


def test_recaptcha_markup_on_short_real_page_is_not_a_phrase_match():
    raw = "<html><body><div class='g-recaptcha'></div><p>Short doc.</p></body></html>"
    assert "Short doc." in t.to_text(raw, "html")


def test_long_helpcenter_article_with_phrase_passes():
    body = "<p>Please confirm your identity before continuing.</p>" + "<p>Real documentation sentence.</p>" * 120
    raw = json.dumps({"article": {"title": "T", "body": body}})
    assert "Real documentation" in t.to_text(raw, "json-helpcenter")
