"""HTTP fetch with a 24-hour disk cache.

States: live (network fetch succeeded this run), cached (fresh <24h cache hit, no request),
stale (cache served after a failed fetch or offline), missing.
"""
import datetime as dt
import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import NamedTuple, Optional

from . import textconv

CACHE = Path(os.environ.get("PROMPTGREMLIN_CACHE", Path.home() / ".cache" / "promptgremlin"))
TIMEOUT = 12
MAX_AGE = dt.timedelta(hours=24)
# Honest, identifying user agent. Never a browser string.
DEFAULT_UA = "promptgremlin/3.4 (+https://github.com/dean815/promptgremlin)"


class Fetched(NamedTuple):
    text: Optional[str]
    state: str            # "live" | "cached" | "stale" | "missing"
    date: Optional[str]   # ISO date the text was fetched
    error: Optional[str] = None
    time: Optional[str] = None  # HH:MM the text was fetched


SOURCES = Path(__file__).resolve().parents[2] / "sources.json"
# Hosts the code itself names, besides the ones in sources.json: the scoreboard and LiveBench.
FIXED_HOSTS = frozenset({"raw.githubusercontent.com", "livebench.ai"})
_HOSTS = None


def allowed_hosts():
    """The hosts the README and PRIVACY.md list: every https host in sources.json, the fixed
    two, and the host of a scoreboard URL the person set themselves. Nothing else is fetched."""
    global _HOSTS
    if _HOSTS is None:
        hosts = set(FIXED_HOSTS)

        def walk(x):
            if isinstance(x, dict):
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
            elif isinstance(x, str) and x.startswith("https://"):
                hosts.add(urllib.parse.urlsplit(x).hostname)
        try:
            walk(json.loads(SOURCES.read_text(encoding="utf-8")))
        except (OSError, ValueError):
            pass
        _HOSTS = frozenset(h for h in hosts if h)
    own = os.environ.get("PROMPTGREMLIN_SCOREBOARD_URL", "")
    return _HOSTS | ({urllib.parse.urlsplit(own).hostname} if own.startswith("https://") else set())


def _allowed(url):
    return (isinstance(url, str) and url.startswith("https://")
            and urllib.parse.urlsplit(url).hostname in allowed_hosts())


class _HttpsOnlyRedirects(urllib.request.HTTPRedirectHandler):
    """Follow a redirect only to an https:// address on one of the listed hosts."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not _allowed(newurl):
            raise urllib.error.HTTPError(newurl, code, f"redirect to an unlisted or non-https address "
                                         f"refused: {newurl[:80]!r}", headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OPENER = urllib.request.build_opener(_HttpsOnlyRedirects)


def _open(req, timeout):
    return _OPENER.open(req, timeout=timeout)


def _http_get(url):
    # Only https. urllib also reads file:// and other schemes, so refuse them before it runs.
    if not isinstance(url, str) or not url.startswith("https://"):
        raise ValueError(f"only https:// URLs are fetched, not {str(url)[:80]!r}")
    if not _allowed(url):
        raise ValueError(f"host not on the documented list: {str(url)[:80]!r}")
    req = urllib.request.Request(url, headers={
        "User-Agent": DEFAULT_UA,
        "Accept": "text/markdown, text/plain, application/json, text/html;q=0.8",
    })
    with _open(req, TIMEOUT) as r:
        data = r.read()
        charset = r.headers.get_content_charset() or "utf-8"
        try:
            return data.decode(charset, "replace")
        except LookupError:
            return data.decode("utf-8", "replace")


def _paths(url):
    key = hashlib.sha1(url.encode()).hexdigest()[:16]
    return CACHE / f"{key}.txt", CACHE / f"{key}.json"


def _read_cache(url):
    body, meta = _paths(url)
    if not body.exists():
        return None
    try:
        fetched_at = dt.datetime.fromisoformat(json.loads(meta.read_text(encoding="utf-8"))["fetched_at"])
    except Exception:
        return None
    return body.read_text(encoding="utf-8"), fetched_at


def fetch(url, fmt, offline=False, now=None, get=None, force=False):
    now = now or dt.datetime.now()
    get = get or _http_get
    cached = _read_cache(url)
    if cached and not offline and not force and now - cached[1] < MAX_AGE:
        return Fetched(cached[0], "cached", cached[1].date().isoformat(), None,
                       cached[1].strftime("%H:%M"))
    error = None
    if not offline:
        try:
            text = textconv.to_text(get(url), fmt)
            body, meta = _paths(url)
            CACHE.mkdir(parents=True, exist_ok=True)
            body.write_text(text, encoding="utf-8")
            meta.write_text(json.dumps({"url": url, "fetched_at": now.isoformat(timespec="seconds")}),
                            encoding="utf-8")
            return Fetched(text, "live", now.date().isoformat(), None, now.strftime("%H:%M"))
        except Exception as e:
            error = f"{type(e).__name__}: {e}"[:200]
    if cached:
        return Fetched(cached[0], "stale", cached[1].date().isoformat(), error,
                       cached[1].strftime("%H:%M"))
    return Fetched(None, "missing", None, error)
