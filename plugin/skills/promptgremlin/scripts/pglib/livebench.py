"""LiveBench scores and realised cost per task, fetched on the person's machine.

The snapshot carries only the release id: LiveBench states no data licence, so its numbers are
read straight from livebench.ai and never republished.
"""
import csv
import io
import re
from typing import NamedTuple, Optional

from . import fetch
from .names import canonical

SUITES = ("long_agentic", "reasoning", "coding", "browser", "data_analysis", "research", "design")
STATES = ("live", "cached", "stale", "missing")
EFFORT = "max"  # LiveBench runs every model at its highest supported effort.
# The host is fixed here, never read from the fetched snapshot, and a release is eight digits.
BASE = "https://livebench.ai/data/"
RELEASE = re.compile(r"[0-9]{8}")


class Loaded(NamedTuple):
    metrics: dict           # {model id: {"livebench:<suite>": {"score", "cost_per_task", "effort"}}}
    state: str              # the worse of the fetches that worked; missing without table.csv
    date: Optional[str]     # the older of their dates
    unmapped: list          # LiveBench names with no alias


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _rows(text):
    """{model: row}, or None when the CSV can't be parsed (a field past csv's size limit, say)."""
    try:
        return {r["model"]: r for r in csv.DictReader(io.StringIO(text))
                if isinstance(r.get("model"), str) and r["model"]}
    except csv.Error:
        return None


def _cost(row, suite):
    """Suite cost over its question count; None when either column is absent or zero."""
    cost, nq = _num((row or {}).get(suite)), _num((row or {}).get(f"nq_{suite}"))
    return round(cost / nq, 4) if cost is not None and nq else None


def pick_release(fetched, bundled):
    """The snapshot's release if it is eight digits, else the bundled snapshot's, else None."""
    for r in (fetched, bundled):
        if isinstance(r, str) and RELEASE.fullmatch(r):
            return r
    return None


def load(release, aliases, offline, now, get=None):
    if not (isinstance(release, str) and RELEASE.fullmatch(release)):
        return Loaded({}, "missing", None, [])
    got = [fetch.fetch(f"{BASE}{release}/{name}.csv", "csv", offline=offline, now=now, get=get)
           for name in ("table", "cost")]
    if got[0].state == "missing":
        return Loaded({}, "missing", None, [])
    # Without cost.csv the scores still count; cost per task falls back to list price.
    got = [g for g in got if g.state != "missing"]
    state = max((g.state for g in got), key=STATES.index)
    table, costs = _rows(got[0].text), _rows(got[1].text) if len(got) > 1 else {}
    if table is None:
        return Loaded({}, "missing", None, [])
    costs = costs or {}
    metrics, unmapped = {}, []
    for name, row in table.items():
        mid = canonical("livebench", name, aliases)
        if mid is None:
            unmapped.append(name)
            continue
        for suite in SUITES:
            score = _num(row.get(suite))
            if score is None:
                continue
            m = {"score": score, "effort": EFFORT}
            cpt = _cost(costs.get(name), suite)
            if cpt is not None:
                m["cost_per_task"] = cpt
            metrics.setdefault(mid, {})[f"livebench:{suite}"] = m
    return Loaded(metrics, state, min(g.date for g in got), unmapped)
