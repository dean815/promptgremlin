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
    assert r.state == "live" and r.date == "2026-10-01" and r.time == "09:00"
    assert "body" in r.text and "<Tip>" not in r.text
    assert calls == ["https://x/a.md"]


def test_fresh_cache_skips_network():
    _fresh_cache()
    f.fetch("u", "md", get=lambda u: "# A", now=NOW)
    r = f.fetch("u", "md", get=_boom, now=NOW + dt.timedelta(hours=3))
    assert r.state == "cached" and r.text == "# A"
    assert r.date == "2026-10-01" and r.time == "09:00" and r.error is None


def test_stale_cache_served_when_network_fails():
    _fresh_cache()
    f.fetch("u", "md", get=lambda u: "# A", now=NOW)
    r = f.fetch("u", "md", get=_down, now=NOW + dt.timedelta(days=2))
    assert r.state == "stale" and r.date == "2026-10-01"
    assert "OSError" in r.error


def test_offline_uses_old_cache_without_network():
    _fresh_cache()
    f.fetch("u", "md", get=lambda u: "# A", now=NOW)
    r = f.fetch("u", "md", offline=True, get=_boom, now=NOW + dt.timedelta(days=30))
    assert r.state == "stale" and r.text == "# A"


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

    orig = f._open
    try:
        f._open = lambda req, timeout=0: Resp("café".encode("latin-1"), "latin-1")
        assert f._http_get("https://livebench.ai/x") == "café"
        f._open = lambda req, timeout=0: Resp("café".encode("utf-8"), None)
        assert f._http_get("https://livebench.ai/x") == "café"
        f._open = lambda req, timeout=0: Resp(b"abc", "no-such-codec")
        assert f._http_get("https://livebench.ai/x") == "abc"
    finally:
        f._open = orig


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
    assert r.state == "stale" and "bot challenge page" in r.error
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
    assert r.state == "stale" and r.text == "# Old" and "OSError" in r.error


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

    real = f._open
    f._open = fake_urlopen
    try:
        assert f._http_get("https://livebench.ai/a") == "ok"
    finally:
        f._open = real
    assert seen["user-agent"] == f.DEFAULT_UA
    repo = json.loads((Path(__file__).resolve().parents[4] / ".claude-plugin" / "plugin.json").read_text())["repository"]
    assert f.DEFAULT_UA == f"promptgremlin/3.4 (+{repo})"
    assert f.DEFAULT_UA.startswith("promptgremlin/3.4 (+https://github.com/")
    assert "Mozilla" not in seen["user-agent"]
    assert not hasattr(f, "BROWSER_UA")


def test_http_get_refuses_every_scheme_but_https_before_opening():
    import urllib.request

    def boom(req, timeout=None):
        raise AssertionError("_open called")

    real = f._open
    f._open = boom
    try:
        for url in ("file:///etc/hosts", "file:///etc/hosts#x", "http://example.com/a",
                    "ftp://example.com/a", "data:text/plain,hi", "/etc/hosts", " https://x"):
            try:
                f._http_get(url)
            except ValueError as e:
                assert "https" in str(e)
            else:
                raise AssertionError(f"{url} was not refused")
    finally:
        f._open = real


def test_redirects_are_followed_only_to_listed_https_hosts():
    import urllib.error
    import urllib.request

    h = f._HttpsOnlyRedirects()
    req = urllib.request.Request("https://livebench.ai/x", headers={"User-Agent": f.DEFAULT_UA})
    ok = h.redirect_request(req, None, 302, "Found", {}, "https://en.wikipedia.org/y")
    assert ok.full_url == "https://en.wikipedia.org/y"
    for bad in ("http://livebench.ai/y", "ftp://b.example/y", "file:///etc/hosts",
                "https://b.example/y", "https://livebench.ai.evil.example/y"):
        try:
            h.redirect_request(req, None, 302, "Found", {}, bad)
        except urllib.error.HTTPError as e:
            assert "refused" in str(e)
        else:
            raise AssertionError(f"redirect to {bad} was followed")
    # The opener the fetcher uses carries this handler in place of the default one.
    kinds = [type(x) for x in f._OPENER.handlers]
    assert f._HttpsOnlyRedirects in kinds and urllib.request.HTTPRedirectHandler not in kinds


def test_fetch_of_a_file_url_is_missing_and_reads_nothing():
    _fresh_cache()
    r = f.fetch(Path(__file__).resolve().as_uri(), "md", now=NOW)
    assert r.state == "missing" and r.text is None and "ValueError" in r.error


def test_only_listed_hosts_are_fetched():
    hosts = f.allowed_hosts()
    assert {"raw.githubusercontent.com", "livebench.ai", "en.wikipedia.org"} <= hosts
    real = f._open

    def never(req, timeout):
        raise AssertionError(f"request went out for {req.full_url}")
    f._open = never
    try:
        try:
            f._http_get("https://b.example/page")
        except ValueError as e:
            assert "documented list" in str(e)
        else:
            raise AssertionError("an unlisted host was fetched")
    finally:
        f._open = real
