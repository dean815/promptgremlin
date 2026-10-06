import datetime as dt
import json
import tempfile
from pathlib import Path

from pglib import fetch as f

NOW = dt.datetime(2026, 10, 1, 9, 0)


def _fresh_cache():
    f.CACHE = Path(tempfile.mkdtemp())


def _boom(url):
    raise AssertionError("network called")


def _down(url):
    raise OSError("offline")


def test_live_fetch_converts():
    _fresh_cache()
    calls = []

    def get(url):
        calls.append((url))
        return "# Hi\n<Tip>\nbody\n</Tip>"

    r = f.fetch("https://x/a.md", "md", get=get, now=NOW)
    assert r.state == "live" and r.date == "2026-10-01"
    assert "body" in r.text and "<Tip>" not in r.text
    assert calls == ["https://x/a.md"]


def test_fresh_cache_skips_network():
    _fresh_cache()
    f.fetch("u", "md", get=lambda u: "# A", now=NOW)
    r = f.fetch("u", "md", get=_boom, now=NOW + dt.timedelta(hours=3))
    assert r.state == "live" and r.text == "# A"


def test_stale_cache_served_when_network_fails():
    _fresh_cache()
    f.fetch("u", "md", get=lambda u: "# A", now=NOW)
    r = f.fetch("u", "md", get=_down, now=NOW + dt.timedelta(days=2))
    assert r.state == "cache" and r.date == "2026-10-01"
    assert "OSError" in r.error


def test_offline_uses_old_cache_without_network():
    _fresh_cache()
    f.fetch("u", "md", get=lambda u: "# A", now=NOW)
    r = f.fetch("u", "md", offline=True, get=_boom, now=NOW + dt.timedelta(days=30))
    assert r.state == "cache" and r.text == "# A"


def test_missing_when_no_network_and_no_cache():
    _fresh_cache()
    r = f.fetch("u", "md", get=_down, now=NOW)
    assert r.state == "missing" and r.text is None and "OSError" in r.error


def test_html_shell_is_a_failed_fetch():
    _fresh_cache()
    r = f.fetch("u", "md", get=lambda u: "<!doctype html><html>spa</html>", now=NOW)
    assert r.state == "missing" and "ValueError" in r.error


def test_http_get_decodes_with_response_charset(monkeypatch=None):
    import io
    import urllib.request

    class Resp(io.BytesIO):
        def __init__(self, data, charset):
            super().__init__(data)
            self.headers = type("H", (), {"get_content_charset": lambda s: charset})()

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    orig = urllib.request.urlopen
    try:
        urllib.request.urlopen = lambda req, timeout=0: Resp("café".encode("latin-1"), "latin-1")
        assert f._http_get("https://x") == "café"
        urllib.request.urlopen = lambda req, timeout=0: Resp("café".encode("utf-8"), None)
        assert f._http_get("https://x") == "café"
        urllib.request.urlopen = lambda req, timeout=0: Resp(b"abc", "no-such-codec")
        assert f._http_get("https://x") == "abc"
    finally:
        urllib.request.urlopen = orig


def test_cache_roundtrips_non_ascii():
    _fresh_cache()
    f.fetch("https://x/u.md", "md", get=lambda u: "# café — 日本", now=NOW)
    r = f.fetch("https://x/u.md", "md", offline=True, now=NOW)
    assert r.text == "# café — 日本"


CHALLENGE = "<html><body><h1>Please confirm your identity</h1></body></html>"


def test_bot_challenge_with_cache_returns_cache_with_error():
    _fresh_cache()
    f.fetch("u", "html", get=lambda u: "<html><body><h1>Doc</h1><p>Real.</p></body></html>", now=NOW)
    r = f.fetch("u", "html", get=lambda u: CHALLENGE, now=NOW + dt.timedelta(days=2))
    assert r.state == "cache" and "bot challenge page" in r.error
    assert "Real." in r.text


def test_bot_challenge_without_cache_is_missing():
    _fresh_cache()
    r = f.fetch("u", "html", get=lambda u: CHALLENGE, now=NOW)
    assert r.state == "missing" and "bot challenge page" in r.error


def test_force_bypasses_fresh_cache_and_updates_it():
    _fresh_cache()
    f.fetch("u", "md", get=lambda u: "# Old", now=NOW)
    r = f.fetch("u", "md", force=True, get=lambda u: "# New", now=NOW + dt.timedelta(hours=1))
    assert r.state == "live" and r.text == "# New"
    assert f.fetch("u", "md", get=_boom, now=NOW + dt.timedelta(hours=2)).text == "# New"


def test_force_falls_back_to_cache_with_error_when_network_fails():
    _fresh_cache()
    f.fetch("u", "md", get=lambda u: "# Old", now=NOW)
    r = f.fetch("u", "md", force=True, get=_down, now=NOW + dt.timedelta(hours=1))
    assert r.state == "cache" and r.text == "# Old" and "OSError" in r.error


def test_http_get_sends_only_the_honest_identifying_ua():
    import io
    import urllib.request
    seen = {}

    class _Resp(io.BytesIO):
        headers = type("H", (), {"get_content_charset": staticmethod(lambda: "utf-8")})()
        def __enter__(self): return self
        def __exit__(self, *a): return False

    def fake_urlopen(req, timeout=None):
        seen.update({k.lower(): v for k, v in req.header_items()})
        return _Resp(b"ok")

    real = urllib.request.urlopen
    urllib.request.urlopen = fake_urlopen
    try:
        assert f._http_get("https://x/a") == "ok"
    finally:
        urllib.request.urlopen = real
    assert seen["user-agent"] == f.DEFAULT_UA
    repo = json.loads((Path(__file__).resolve().parents[4] / ".claude-plugin" / "plugin.json").read_text())["repository"]
    assert f.DEFAULT_UA == f"promptgremlin/2.0 (+{repo})"
    assert f.DEFAULT_UA.startswith("promptgremlin/2.0 (+https://github.com/")
    assert "Mozilla" not in seen["user-agent"]
    assert not hasattr(f, "BROWSER_UA")
