import datetime as dt
import json
import tempfile
from pathlib import Path

from pglib import fetch
from pglib import livebench as L

HERE = Path(__file__).resolve().parent
FIX = HERE / "fixtures"
ALIASES = json.loads((HERE.parents[1] / "model_aliases.json").read_text(encoding="utf-8"))
NOW = dt.datetime(2026, 10, 28, 9, 0)
BASE = "https://livebench.ai/data/"
RELEASE = "20261025"


def _fresh_cache():
    fetch.CACHE = Path(tempfile.mkdtemp())


def _fixture_get(table=None, cost=None):
    files = {f"{BASE}{RELEASE}/table.csv": table or (FIX / "livebench_table.csv").read_text(encoding="utf-8"),
             f"{BASE}{RELEASE}/cost.csv": cost or (FIX / "livebench_cost.csv").read_text(encoding="utf-8")}

    def get(url):
        assert url in files, f"unexpected network call: {url}"
        return files[url]
    return get


def _load(**kw):
    _fresh_cache()
    return L.load(RELEASE, BASE, ALIASES, False, NOW, get=_fixture_get(**kw))


def test_scores_and_cost_per_task_from_fixtures():
    r = _load()
    assert r.state == "live" and r.date == "2026-10-28"
    opus = r.metrics["claude-opus-5-5"]["livebench:coding"]
    # Live cost.csv: coding suite $145.8927 over 29 questions.
    assert opus == {"score": 96.3, "cost_per_task": round(145.8927 / 29, 4), "effort": "max"}
    sol = r.metrics["gpt-6-1-sol"]["livebench:long_agentic"]
    assert sol["score"] == 68.7 and sol["cost_per_task"] == round(116.7779 / 18, 4)
    assert set(r.metrics["claude-haiku-5-5"]) == {f"livebench:{s}" for s in L.SUITES}


def test_unknown_models_are_skipped_and_reported():
    r = _load()
    assert r.unmapped == ["inkling"]
    assert not any("inkling" in k for k in r.metrics)


def test_missing_nq_column_keeps_score_without_cost():
    text = (FIX / "livebench_cost.csv").read_text(encoding="utf-8").splitlines()
    head = text[0].split(",")
    i = head.index("nq_coding")
    cost = "\n".join(",".join(c for j, c in enumerate(line.split(",")) if j != i) for line in text)
    r = _load(cost=cost)
    coding = r.metrics["claude-opus-5-5"]["livebench:coding"]
    assert coding == {"score": 96.3, "effort": "max"}
    assert "cost_per_task" in r.metrics["claude-opus-5-5"]["livebench:design"]


def test_failing_get_with_no_cache_is_missing():
    _fresh_cache()

    def down(url):
        raise OSError("offline")
    assert tuple(L.load(RELEASE, BASE, ALIASES, False, NOW, get=down)) == ({}, "missing", None, [])


def test_failed_cost_fetch_keeps_scores_without_cost():
    _fresh_cache()
    table = _fixture_get()

    def get(url):
        if url.endswith("cost.csv"):
            raise OSError("404")
        return table(url)
    r = L.load(RELEASE, BASE, ALIASES, False, NOW, get=get)
    assert r.state == "live" and r.date == "2026-10-28"
    assert r.metrics["claude-opus-5-5"]["livebench:coding"] == {"score": 96.3, "effort": "max"}
    assert not any("cost_per_task" in m for ms in r.metrics.values() for m in ms.values())


def test_failed_table_fetch_is_missing():
    _fresh_cache()
    cost = _fixture_get()

    def get(url):
        if url.endswith("table.csv"):
            raise OSError("404")
        return cost(url)
    assert tuple(L.load(RELEASE, BASE, ALIASES, False, NOW, get=get)) == ({}, "missing", None, [])


def test_state_is_the_worse_of_the_two_fetches():
    _fresh_cache()
    get = _fixture_get()
    fetch.fetch(f"{BASE}{RELEASE}/table.csv", "csv", now=NOW - dt.timedelta(days=2), get=get)
    fetch.fetch(f"{BASE}{RELEASE}/cost.csv", "csv", now=NOW - dt.timedelta(hours=2), get=get)
    r = L.load(RELEASE, BASE, ALIASES, True, NOW, get=get)
    assert r.state == "stale" and r.date == "2026-10-26"
    assert r.metrics["claude-opus-5-5"]["livebench:coding"]["score"] == 96.3


def test_no_release_is_missing_without_fetching():
    def boom(url):
        raise AssertionError("network called")
    assert tuple(L.load(None, BASE, ALIASES, False, NOW, get=boom)) == ({}, "missing", None, [])
