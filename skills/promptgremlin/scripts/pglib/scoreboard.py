"""Score candidate models for a task type from the daily snapshot, and print the suggestion.

Every model number a person sees is printed here; the writer copies it and never computes one.
"""
import copy
import datetime as dt
import json
import os
import re
from pathlib import Path
from typing import NamedTuple, Optional

from . import fetch
from . import notes as N

ENV = "PROMPTGREMLIN_SCOREBOARD_URL"
DEFAULT_URL = "https://raw.githubusercontent.com/dean815/promptgremlin/scoreboard/scoreboard.json"


def scoreboard_url():
    """Read at call time so tests and guidance.py can point it at a fixture."""
    return os.environ.get(ENV, DEFAULT_URL)


SCOREBOARD_URL = scoreboard_url()
VALUE_WIN = 0.70        # best value: voters prefer the best pick over it at most this often...
VALUE_SHARE = 0.85      # ...or, on a scored main metric, it has this share of the best's score
XV_QUALITY_GAP = 0.05   # cross-vendor line: this much better on the 0-1 scale...
XV_COST_RATIO = 0.6     # ...or at most this share of the target's best-value cost
IMPACT_RATIO = 1 / 3   # an option at this share of the best's cost or less makes the question high-impact
THIN = 0.5              # coverage under this share of the type's weights is thin evidence
BUDGET = 1200
EFFORT_ORDER = ("minimal", "low", "medium", "high", "xhigh", "max")
# SKILL.md's agent tools; build, change-code and agent default to one.
AGENT_TOOLS = ("claude-code", "codex", "gemini-cli", "cursor", "copilot", "lovable", "replit", "manus")
AGENT_TYPES = ("build", "change-code", "agent")
# The media types' tools (types/image.md and video.md slot 1). They host no family: each one's
# own notes list its models, and with no target named they are the pool.
MEDIA_TOOLS = {"image": ("gpt-image", "nano-banana", "midjourney"),
               "video": ("google-video", "sora", "runway", "kling", "higgsfield")}
SOURCES = {"lmarena": "LMArena", "livebench": "LiveBench", "epoch": "Epoch"}
WORDS = {"webdev": "WebDev", "eci": "ECI"}
LMARENA_URL = "https://lmarena.ai/leaderboard"


class Loaded(NamedTuple):
    snapshot: Optional[dict]
    state: str              # live | cached | stale | bundled | missing
    date: Optional[str]     # the snapshot's build date


class Candidate(NamedTuple):
    tool: Optional[str]     # None when the target is a family
    model: str


class Pick(NamedTuple):
    tool: Optional[str]
    model: str
    name: str
    effort: Optional[str]
    q: Optional[float]      # None: no data
    coverage: float
    used: list              # [(metric key, row)], main metric first
    main: Optional[dict]    # the main metric's row, for ties and win rates
    costs: dict             # {basis: value} for every basis the model has
    cost: Optional[float] = None    # on the basis the selection compared
    basis: Optional[str] = None
    raw: Optional[float] = None     # q without the clamp at 30th place, to order models below it


class Info(NamedTuple):
    type: str
    pool: str               # target | all
    date: Optional[str]     # snapshot date
    state: str              # snapshot freshness
    lb: dict                # {"release", "state"} of the LiveBench fetch
    target: Optional[str] = None    # the named target, for pool target


class Suggestion(NamedTuple):
    best: Optional[Pick]
    value: Optional[Pick]   # None when it is the best-quality model
    session: Optional[Pick]
    also: Optional[Pick]
    thin: list
    ties: list
    flags: list
    nodata: list
    info: Info
    sources: dict
    no_costs: bool = False  # value is None because no other model's cost compares with best's
    session_off: Optional[str] = None   # the session model, when the named target can't run it
    impact: Optional[str] = None        # high: SKILL asks the question in round one; low: veto list


def load_snapshot(skill_dir, offline, now, get=None):
    got = fetch.fetch(scoreboard_url(), "json", offline=offline, now=now, get=get)
    snap, state = None, got.state
    if got.text:
        try:
            snap = json.loads(got.text)
        except ValueError:
            snap = None
    if not isinstance(snap, dict) or "models" not in snap:
        try:
            snap = json.loads((Path(skill_dir) / "scoreboard.json").read_text(encoding="utf-8"))
            state = "bundled"
        except (OSError, ValueError):
            return Loaded(None, "missing", None)
    return Loaded(snap, state, (snap.get("built_at") or "")[:10] or None)


def add_livebench(snapshot, metrics):
    """LiveBench joins at load time, on the person's machine, never in the published file."""
    snap = copy.deepcopy(snapshot)
    for mid, ms in metrics.items():
        if mid in snap["models"]:
            snap["models"][mid].setdefault("metrics", {}).update(ms)
    return snap


LEVEL = r"`?(minimal|low|medium|high|xhigh|max)`?"


def _tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def _names(text):
    """'3.8 and 3.6 Flash' -> ['3.8 Flash', '3.6 Flash']: a bare version borrows the last name's
    words."""
    parts = [p.strip(" `") for p in re.split(r",\s*|\s+and\s+", text) if p.strip(" `")]
    tail = " ".join(w for w in parts[-1].split() if not re.fullmatch(r"[\d.]+", w)) if parts else ""
    return [f"{p} {tail}" if re.fullmatch(r"[\d.]+", p) and tail else p for p in parts]


def _matches(name, label):
    want, have = _tokens(name), _tokens(label)
    return bool(want) and any(have[i:i + len(want)] == want for i in range(len(have) - len(want) + 1))


def _clause_levels(clause):
    """[(name or None, level)] from 'Opus 5.5 medium; Sonnet 5.5 high, ...' or from
    '`medium` on 3.8 and 3.6 Flash, `minimal` on ...'. None is a bare, family-wide level."""
    out = []
    if re.search(LEVEL + r"\s+on\s", clause):
        for m in re.finditer(LEVEL + r"\s+on\s+(.+?)(?=,\s*" + LEVEL + r"\s+on\s|$)", clause):
            out += [(n, m.group(1)) for n in _names(m.group(2))]
        return out
    for part in clause.split(";"):
        part = part.strip()
        if re.fullmatch(LEVEL, part):
            out.append((None, part.strip("`")))
            continue
        m = re.match(r"(.+?)\s+" + LEVEL + r"\b", part)
        if m:
            out += [(n, m.group(2)) for n in _names(m.group(1))]
    return out


def note_efforts(block, models):
    """{model id: level} from a notes Effort block, which wins over OpenRouter's default (design,
    Risks). Its 'Start:' clause (the starting level) first, then its 'Default(s)' clause; a bare
    level there covers every model not named. A parenthesised '(default x)' belongs to one line,
    not the family, and is skipped. models: {id: display name}."""
    found = {}
    for m in re.finditer(r"(?<!\()\b(Start|Defaults?)\b:?\s*(.*?)(?:\.(?=\s|$)|$)", block or "", re.M):
        found.setdefault(m.group(1).rstrip("s"), _clause_levels(m.group(2)))
    out = {}
    for mid, name in models.items():
        for kind in ("Start", "Default"):
            hits = [(len(_tokens(n)), lv) for n, lv in found.get(kind, [])
                    if n and (_matches(n, name) or _matches(n, mid))]
            if hits:
                out[mid] = max(hits)[1]
                break
        else:
            bare = [lv for n, lv in found.get("Default", []) if n is None]
            if bare:
                out[mid] = bare[0]
    return out


def add_note_efforts(snapshot, reg, notes_dir):
    """Each family's notes Effort block joins at load time as efforts.notes; where the snapshot's
    default (OpenRouter's) disagrees, an EFFORT-MISMATCH flag says so."""
    snap = copy.deepcopy(snapshot)
    for key, e in reg.items():
        path = Path(notes_dir) / f"{key}.md"
        if e.get("kind") != "family" or not path.exists():
            continue
        n = N.load(path)
        ids = {m: snap["models"][m].get("name", m) for m in N.model_ids(n) if m in snap["models"]}
        for mid, level in note_efforts(n.blocks.get("Effort"), ids).items():
            eff = snap["models"][mid].get("efforts") or {}
            snap["models"][mid]["efforts"] = eff
            eff["notes"] = level
            if eff.get("default") and eff["default"] != level:
                src = eff.get("default_from") or "snapshot"
                snap.setdefault("flags", []).append(f"EFFORT-MISMATCH {mid} notes {level} {src} {eff['default']}")
    return snap


def session_id(name, snapshot):
    """The snapshot id for the model a host names its own way ('Claude Opus 5.5 1m', 'Opus 5.5
    (1M context)'): a context-size suffix dropped, then an exact id or name, else the one id
    ending in it. Never the nearest version: 'Claude Sonnet 5' is not claude-sonnet-5-5. A name
    that matches nothing passes through unchanged."""
    q = re.sub(r"[^a-z0-9.\s_/-]+", " ", name.lower())
    q = re.sub(r"[\s_./]+", "-", q).strip("-")
    q = re.sub(r"(-\d+[km])?(-context)?$", "", re.sub(r"-+", "-", q))
    models = snapshot.get("models", {})
    if q in models:
        return q
    named = [m for m, e in models.items() if re.sub(r"[\s_./]+", "-", e.get("name", "").lower()) == q]
    hits = named or [m for m in models if m.endswith("-" + q)]
    return hits[0] if len(hits) == 1 else name


def win_rate(delta):
    return 1 / (1 + 10 ** (-delta / 400))


def _value(row):
    return row.get("elo") if "elo" in row else row.get("score")


def scale(value, board, clamp=True):
    """0 at the board's 30th place, 1 at its top. Unclamped, it keeps the order below 30th."""
    top, p30 = board["top"], board["p30"]
    if top == p30:
        return 1.0 if value >= top else (0.0 if clamp else value - top)
    x = (value - p30) / (top - p30)
    return min(1.0, max(0.0, x)) if clamp else x


def boards(snapshot):
    """The snapshot's stored board scales, plus LiveBench's: zero to the release's best score,
    since the client holds the whole release. No other scale is guessed from our own models."""
    out = dict(snapshot.get("boards", {}))
    for m in snapshot["models"].values():
        for key, row in m.get("metrics", {}).items():
            if key.startswith("livebench:") and isinstance(row, dict) and row.get("score") is not None:
                top = max(out.get(key, {}).get("top", row["score"]), row["score"])
                out[key] = {"top": top, "p30": 0}
    return out


def _rank(effort):
    effort = "high" if effort == "thinking" else effort
    return EFFORT_ORDER.index(effort) if effort in EFFORT_ORDER else EFFORT_ORDER.index("medium")


def pick_variant(rows, effort, default=None):
    """The row at the effort, else the nearest (the higher on a tie). An unlabelled row is the
    model's default effort."""
    if isinstance(rows, dict) or not rows:
        return rows or None
    want = effort or default
    if want is None:
        return max(rows, key=_value)
    eff = lambda r: _rank(r.get("effort") or default)
    return min(rows, key=lambda r: (abs(eff(r) - _rank(want)), -eff(r)))


def resolve_evidence(evidence, type_, slots):
    """The type's block with each matching slot's fields replacing the base's."""
    base = evidence[type_]
    out = {k: v for k, v in base.items() if k != "slots"}
    for cond, mod in base.get("slots", {}).items():
        name, _, want = cond.partition("=")
        got = slots.get(name)
        if got is None or (want != "*" and got != want):
            continue
        for k, v in mod.items():
            out[k] = {m.replace("{" + name + "}", got): w for m, w in v.items()} if isinstance(v, dict) else v
    return out


# The person's words for the image style slots, most specific first: legible text decides the
# board even in "a logo with text".
STYLE_WORDS = {
    "text_rendering": ("text", "lettering", "typography", "words", "font", "signage"),
    "photorealistic": ("photo", "photos", "photograph", "photographic", "photography", "photoreal", "realistic"),
    "portraits": ("portrait", "headshot", "headshots"),
    "3d_modeling": ("3d", "cgi", "modeling", "modelling"),
    "commercial_design": ("commercial", "logo", "poster", "product", "packaging", "advert", "banner", "brand"),
    "cartoon": ("cartoon", "anime", "comic", "manga"),
    "art": ("art", "artwork", "illustration", "illustrated", "painting", "drawing"),
}


def style_slot(text, block):
    """The type's style slot value for the person's free-text style ('text rendering', 'photo',
    '3D'), else the text itself, which matches no slot and leaves the base evidence."""
    t = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    values = [c.partition("=")[2] for c in block.get("slots", {}) if c.startswith("style=")]
    if t in values:
        return t
    words = set(t.split("_"))
    for value, said in STYLE_WORDS.items():
        if value in values and words & (set(said) | {value}):
            return value
    return t


def _weights(ev):
    return [kw for part in ("main", "support")
            for kw in sorted(ev.get(part, {}).items(), key=lambda kw: -kw[1])]


def main_key(ev):
    return _weights(ev)[0][0] if ev.get("main") else None


def quality(model, ev, board_scales, effort):
    """Weighted mean of the scaled metrics the model has, renormalised over their weights."""
    default = (model.get("efforts") or {}).get("default")
    total = have = acc = 0.0
    used = []
    for key, w in _weights(ev):
        total += w
        rows = model.get("metrics", {}).get(key)
        row = pick_variant(rows, effort, default) if rows and key in board_scales else None
        if row is None or _value(row) is None:
            continue
        acc += w * scale(_value(row), board_scales[key])
        have += w
        used.append((key, row))
    if not have:
        return None, 0.0, []
    return acc / have, have / total, used


def raw_quality(used, ev, board_scales):
    """quality() over the same metrics without the clamp at each board's 30th place."""
    w = dict(_weights(ev))
    have = sum(w[k] for k, _ in used)
    return sum(w[k] * scale(_value(r), board_scales[k], clamp=False) for k, r in used) / have if have else None


def _blended(price):
    if not price or price.get("in") is None or price.get("out") is None:
        return None
    return (3 * price["in"] + price["out"]) / 4


def _costs(model, ev):
    """Every basis the model has, most specific first. Token efficiency is the mean LiveBench
    cost per task (its cost-to-list-price factor times list price, which is the same number)."""
    metrics = model.get("metrics", {})
    out = {}
    suite = ev.get("cost_suite")
    row = metrics.get(suite) if suite else None
    if isinstance(row, dict) and row.get("cost_per_task") is not None:
        out[suite] = row["cost_per_task"]
    lb = [v["cost_per_task"] for k, v in metrics.items()
          if k.startswith("livebench:") and isinstance(v, dict) and v.get("cost_per_task") is not None]
    if lb:
        out["token-efficiency"] = round(sum(lb) / len(lb), 4)
    if _blended(model.get("price")) is not None:
        out["list price"] = _blended(model["price"])
    return out


def cost_per_task(model, ev, basis=None):
    for b, v in _costs(model, ev).items():
        if basis in (None, b):
            return v, b
    return None, None


def _priced(p, ref):
    """p priced against ref on the most specific basis the two share, so each comparison is like
    for like; cost None when they share none."""
    basis = next((b for b in ref.costs if b in p.costs), None)
    return p._replace(cost=p.costs.get(basis), basis=basis)


def tied(a, b):
    if not a or not b or None in (a.get("lo"), a.get("hi"), b.get("lo"), b.get("hi")):
        return False
    return a["lo"] <= b["hi"] and b["lo"] <= a["hi"]


def _families(key, reg):
    """The notes that list a target's models: a family's own, a tool's uses and offers families,
    or a media tool's own when it has neither."""
    e = reg[key]
    if e.get("kind") == "family":
        return [key]
    fams = [f for f in e.get("uses", []) + e.get("offers", []) if reg.get(f, {}).get("kind") == "family"]
    return fams or [key]


def candidates(target, reg, notes_dir, pool, type_=None):
    """(tool, model) pairs from the notes' model ids. Pool all is every family, for agent-tool
    types every agent tool paired with its families' models, and for media types every media
    tool with its own models."""
    if pool == "target":
        keys = [target]
    elif type_ in MEDIA_TOOLS:
        keys = [t for t in MEDIA_TOOLS[type_] if t in reg]
    elif type_ in AGENT_TYPES:
        keys = [t for t in AGENT_TOOLS if t in reg]
    else:
        keys = [k for k, e in reg.items() if e.get("kind") == "family"]
    out = []
    for key in keys:
        tool = None if reg[key].get("kind") == "family" else key
        for fam in _families(key, reg):
            path = Path(notes_dir) / f"{fam}.md"
            for mid in (N.model_ids(N.load(path)) if path.exists() else []):
                if Candidate(tool, mid) not in out:
                    out.append(Candidate(tool, mid))
    return out


def _effort(entry, override):
    e = entry.get("efforts") or {}
    levels = e.get("levels") or []
    if override:
        if not levels or override in levels:
            return override
        return min(levels, key=lambda lv: abs(_rank(lv) - _rank(override)))
    return e.get("notes") or e.get("default")


def _pick(c, snapshot, ev, board_scales, effort):
    entry = snapshot["models"].get(c.model)
    if entry is None:
        return Pick(c.tool, c.model, c.model, None, None, 0.0, [], None, {})
    eff = _effort(entry, effort)
    q, cov, used = quality(entry, ev, board_scales, eff)
    main = dict(used).get(main_key(ev))
    return Pick(c.tool, c.model, entry.get("name", c.model), eff, q, cov, used, main, _costs(entry, ev),
                raw=raw_quality(used, ev, board_scales))


def _rank_picks(cands, snapshot, ev, board_scales, effort):
    picks = [_pick(c, snapshot, ev, board_scales, effort) for c in cands]
    ranked = sorted((p for p in picks if p.q is not None), key=lambda p: (-p.q, -p.raw, -p.coverage, p.model))
    # One entry per model: in pool all for agent types, several tools offer the same one.
    return ranked, list(dict.fromkeys(p.model for p in picks if p.q is None))


def _cheapest(picks, ref):
    """Cheapest as a share of ref's cost, each priced against ref on the basis the two share, the
    higher quality on a cost tie. A model sharing no basis with ref is left out, not allowed to
    cancel the comparison. Among picks that all clear the quality bar this is the cheap end of
    the cost/quality Pareto frontier."""
    priced = [q for q in (_priced(p, ref) for p in picks) if q.cost is not None and ref.costs[q.basis]]
    return min(priced, key=lambda p: (p.cost / ref.costs[p.basis], -p.q)) if priced else None


def clears(p, best):
    """The value floor, head to head on the main metric rather than on the 0-1 scale, where the
    leader is 1.0 and most others score far lower: a CI tie, a win rate for the best of at most
    VALUE_WIN, or on a scored metric at least VALUE_SHARE of the best's score."""
    a, b = p.main, best.main
    if a is None or b is None:
        return False
    if tied(a, b):
        return True
    if "elo" in a and "elo" in b:
        return win_rate(b["elo"] - a["elo"]) <= VALUE_WIN
    va, vb = _value(a), _value(b)
    return va is not None and bool(vb) and va >= VALUE_SHARE * vb


def _cheaper(picks, best):
    """Picks priced below best on the basis each shares with it, best quality first."""
    priced = (_priced(p, best) for p in picks)
    return [p for p in priced if p.cost is not None and p.cost < best.costs[p.basis]]


def choose(cands, snapshot, ev, info, effort=None, session=None, others=()):
    b = boards(snapshot)
    ranked, nodata = _rank_picks(cands, snapshot, ev, b, effort)
    best = value = sess = also = None
    ties, no_costs, session_off = [], False, None
    if ranked:
        best = ranked[0]
        ties = [p.model for p in ranked[1:] if tied(best.main, p.main)]
        ok = [p for p in ranked if p is best or p.model in ties or clears(p, best)]
        value = _cheapest(ok, best)
        if value is not None and value.model == best.model and value.tool == best.tool:
            value = None
        if value is None:
            # Nothing cheaper clears the floor: the best of the cheaper models, so both options
            # show unless no model is cheaper (decision 2).
            value = next(iter(_cheaper(ranked[1:], best)), None)
        no_costs = value is None and not any(_priced(p, best).cost is not None for p in ranked[1:])
        no_costs = no_costs and len(ranked) > 1
        basis = value.basis if value else next(iter(best.costs), None)
        best = best._replace(cost=best.costs.get(basis), basis=basis)
        also = _also(cands, others, snapshot, ev, b, effort, best, value) if info.pool == "target" else None
    if session and info.pool == "target" and session not in {c.model for c in cands}:
        session_off = session   # not an option the named target can run (decision 3)
    elif session:
        sess = next((p for p in ranked if p.model == session), None)
        sess = sess or _pick(Candidate(None, session), snapshot, ev, b, effort)
    shown = [p for p in (best, value, sess, also) if p and p.q is not None]
    thin = [p.model for p in shown if p.coverage < THIN]
    flags = _flags(snapshot, shown, ranked, nodata, len(cands), ev, info)
    return Suggestion(best, value, sess, also, thin, ties, flags, nodata, info, snapshot.get("sources", {}),
                      no_costs, session_off, _impact(best, value, sess, also))


def _ratio(p, best):
    """p's cost as a share of best's on the basis the two share, or None."""
    basis = next((b for b in p.costs if b in best.costs), None)
    return p.costs[basis] / best.costs[basis] if basis and best.costs[basis] else None


def _impact(best, value, sess, also):
    """High when an option costs IMPACT_RATIO of the best's or less (the exact ratio, not the
    rounded phrase, which prints "1/3" up to 0.4), or the pick's lead is material: the model
    the person is using now, as its own option, falls below the value floor, or Also consider
    is the clearly better model. A value option merely not tied is not a material lead: it is
    chosen for being cheaper, and below 3x the Recommended line is a fine default."""
    if best is None:
        return None
    for p in (value, sess, also):
        r = _ratio(p, best) if p is not None and p.q is not None and p.model != best.model else None
        if r is not None and r <= IMPACT_RATIO:
            return "high"
    own = sess is not None and sess.q is not None and sess.model not in {best.model, value and value.model}
    if own and not clears(sess, best):
        return "high"
    if also is not None and also.q - best.q >= XV_QUALITY_GAP:
        return "high"
    return "low"


def _also(cands, others, snapshot, ev, b, effort, best, value):
    """The rest of the pool's best when it beats ours by XV_QUALITY_GAP, else its cheapest model
    that still clears the value floor against our best at no more than XV_COST_RATIO of our
    value's cost."""
    mine = {c.model for c in cands}
    ranked, _ = _rank_picks([c for c in others if c.model not in mine], snapshot, ev, b, effort)
    if not ranked:
        return None
    if ranked[0].q - best.q >= XV_QUALITY_GAP:
        return ranked[0]
    ours = value or best
    ok = [p for p in ranked if clears(p, best)]
    pick = _cheapest(ok + [ours], ours)
    if pick is None or pick.model == ours.model:
        return None
    return pick if pick.cost <= XV_COST_RATIO * ours.costs[pick.basis] else None


def _flags(snapshot, shown, ranked, nodata, n, ev, info):
    ids = {p.model for p in shown}
    used = {k for p in shown for k, _ in p.used}
    wanted = [k for k, _ in _weights(ev)]
    on = lambda keys, src: any(k == src or k.startswith(src + "/") or k.split(":")[0] == src for k in keys)
    out, unmapped = [], []
    for f in snapshot.get("flags", []):
        words = f.split()
        if words[0] in ("SOURCE-STALE", "SOURCE-FAIL"):
            if on(used, words[1]):
                out.append(f)
        elif words[0] == "UNMAPPED":
            # A top-30 model on a board this type weighs that maps to nothing: maybe a left-out
            # candidate. Only one rated above every shown pick could have changed the answer.
            # Last, so the budget cuts these first.
            if len(words) > 1 and ":" in words[1] and on(wanted, words[1]):
                if _beats_shown(snapshot, ids, words[1], f):
                    unmapped.append(f)
        elif ids & set(words[1:]):
            out.append(f)
    if n and sum(1 for p in ranked if p.main is None) + len(nodata) > n / 2:
        out.append(f"THIN EVIDENCE {info.type}")
    if info.lb.get("state") == "stale":
        out.append("LIVEBENCH-STALE")
    return out + unmapped


def _beats_shown(snapshot, ids, key, flag):
    """True unless the flag's @rating is at or below a shown pick's rating on that board."""
    m = re.search(r" @(-?[\d.]+)$", flag)
    rows = [r for mid in ids for r in snapshot.get("models", {}).get(mid, {}).get("metrics", {}).get(key, [])]
    vals = [r.get("elo", r.get("score")) for r in rows if r.get("elo", r.get("score")) is not None]
    return not (m and vals) or float(m.group(1)) > max(vals)


def label(key):
    src, _, board = key.partition(":")
    return " ".join([SOURCES.get(src, src)] + [WORDS.get(w, w) for w in re.split(r"[/_]", board)])


def _fmt(row):
    return str(round(row["elo"])) if "elo" in row else f"{row['score']:g}"


def _date(iso):
    d = dt.date.fromisoformat(iso)
    return f"{d:%b} {d.day}"


def _evidence(p, sources):
    out = []
    for key, row in p.used[:2]:
        text = f"{label(key)} {_fmt(row)}"
        pub = sources.get("lmarena", {}).get("published", {}).get(key.partition(":")[2].split("/")[0])
        if key.startswith("lmarena:") and pub:
            text += f" ({_date(pub)})"
        out.append(text)
    return ", ".join(out)


def _who(p, tag=""):
    who = ", ".join(x for x in (p.tool, p.model + tag) if x)
    return who + (f", effort {p.effort}" if p.effort else "")


def _cost_phrase(p, ref, surface, basis=None):
    basis = basis or next((b for b in p.costs if b in ref.costs), None)
    if basis is None or not p.costs.get(basis) or not ref.costs.get(basis):
        return None
    a, b = p.costs[basis], ref.costs[basis]
    r, plan = a / b, surface == "plan"
    if r <= 0.5:
        n = round(1 / r)
        amount = "half" if n == 2 else f"1/{n}"
        lead = f"uses about {amount} as much of your plan" if plan else f"about {amount} the cost"
    elif r < 0.95:
        pct = max(5, round((1 - r) * 20) * 5)
        lead = f"uses about {pct}% less of your plan" if plan else f"about {pct}% cheaper"
    elif r <= 1.05:
        lead = "uses about the same share of your plan" if plan else "about the same cost"
    elif r < 1.5:
        pct = max(5, round((r - 1) * 20) * 5)
        lead = f"uses about {pct}% more of your plan" if plan else f"about {pct}% more"
    else:
        x = f"{r:.1f}".rstrip("0").rstrip(".")
        lead = f"uses about {x}x as much of your plan" if plan else f"about {x}x the cost"
    if basis == "list price":
        how, detail = " by list price", f"${a:.2f} vs ${b:.2f} per M tokens, 3:1 blend"
    else:
        src = "LiveBench mean" if basis == "token-efficiency" else label(basis)
        how, detail = " per task", f"{src} ${a:.2f} vs ${b:.2f}" + (" per task" if plan else "")
    return f"{lead[0].upper()}{lead[1:]}{'' if plan else how} ({detail})"


def _preference(p, ref, key):
    if key is None or ref.main is None:
        return None
    if p.main is None:
        return f"no {label(key)} data"
    if tied(p.main, ref.main):
        return f"statistically tied with {ref.name} on {label(key)}"
    if "elo" in p.main and "elo" in ref.main:
        d = ref.main["elo"] - p.main["elo"]
        if d >= 0:
            return f"voters preferred {ref.name} about {round(win_rate(d) * 100)}% of the time"
        return f"voters preferred it over {ref.name} about {round(win_rate(-d) * 100)}% of the time"
    return f"{label(key)} {_fmt(p.main)} vs {_fmt(ref.main)}"


def _compare(p, ref, key, surface, basis=None):
    parts = [x for x in (_cost_phrase(p, ref, surface, basis), _preference(p, ref, key)) if x]
    text = "; ".join(parts)
    text = text[0].upper() + text[1:] + "." if text else ""
    return text + (" Thin evidence." if p.coverage < THIN else "")


def _list(items, dropped):
    return ", ".join(items) + (f" +{dropped} more" if dropped else "")


def _data_line(s, surface):
    used = {k.split(":")[0] for p in (s.best, s.value, s.session, s.also) if p for k, _ in p.used}
    parts = []
    if "lmarena" in used:
        parts.append(f"LMArena ({s.sources.get('lmarena', {}).get('licence', 'CC BY 4.0')}, {LMARENA_URL})")
    lb, release = s.info.lb, s.info.lb.get("release") or ""
    if lb.get("state") in (None, "missing"):
        parts.append("LiveBench unavailable")
    else:
        when = f"{release[:4]}-{release[4:6]}-{release[6:]}" if len(release) == 8 else release
        parts.append(f"LiveBench {when}" + (" (stale)" if lb.get("state") == "stale" else ""))
    if "epoch" in used:
        parts.append(f"Epoch ({s.sources.get('epoch', {}).get('licence', 'CC BY 4.0')})")
    listed = s.best and s.best.basis == "list price"
    # Prices come from models.dev, effort defaults and the price cross-check from OpenRouter.
    parts.append("models.dev, OpenRouter" + (" (list prices, not measured cost)" if listed else ""))
    tail = " Plans meter usage their own way." if surface == "plan" else ""
    return (f"Data: {', '.join(parts)}; snapshot {s.info.date}. "
            f"Leaderboards average many tasks; yours may differ.{tail}")


def _render(s, surface, priority, flags, nodata, more_flags, more_nodata):
    i, key = s.info, None
    lines = [f"Suggest: {i.type} | pool {i.pool} | snapshot {i.date} ({i.state})"
             + (f" | impact {s.impact}" if s.impact else "")]
    if s.best is None:
        lines.append("Best quality: no candidate has data for this task.")
    else:
        key = s.best.used[0][0] if s.best.used else None
        rec_value = priority == "balanced" and s.value is not None
        rec = lambda on: " (Recommended)" if on else ""
        thin = " Thin evidence." if s.best.coverage < THIN else ""
        lines.append(f"Best quality{rec(not rec_value)}: {_who(s.best)}. {_evidence(s.best, s.sources)}.{thin}")
        if s.value is None and s.no_costs:
            lines.append(f"Best value: no cost data to compare with {s.best.name}.")
        elif s.value is None:
            lines.append("Best value: same as best quality.")
        else:
            lines.append(f"Best value{rec(rec_value)}: {_who(s.value)}. "
                         f"{_compare(s.value, s.best, key, surface, s.best.basis)}")
    p = s.session
    tag = " (the model you're using now)"
    if s.session_off:
        lines.append(f"Session: {s.session_off}{tag} is not offered by {i.target or 'this target'}.")
    if p is not None:
        if s.best and p.model == s.best.model:
            lines.append(f"Session: {p.model}{tag} = best quality.")
        elif s.value and p.model == s.value.model:
            lines.append(f"Session: {p.model}{tag} = best value.")
        elif p.q is None or s.best is None:
            lines.append(f"Session: {p.model}{tag}: no data for this task.")
        else:
            lines.append(f"Session: {_who(p, tag)}. {_compare(p, s.best, key, surface)}")
    if i.pool == "target":
        lines.append(f"Also consider: {_who(s.also)}. {_compare(s.also, s.best, key, surface)}"
                     if s.also else "Also consider: none.")
    if nodata or more_nodata:
        lines.append(f"No data: {_list(nodata, more_nodata)}.")
    lines.append(_data_line(s, surface))
    lines.append(f"Flags: {_list(flags, more_flags) if flags or more_flags else 'none'}")
    return "\n".join(lines)


def render(s, surface="api", priority="quality"):
    """The --suggest block, under BUDGET characters: long flag and no-data lists are cut first."""
    flags, nodata = list(s.flags), list(s.nodata)
    while True:
        text = _render(s, surface, priority, flags, nodata,
                       len(s.flags) - len(flags), len(s.nodata) - len(nodata))
        if len(text) < BUDGET or not (flags or nodata):
            return text
        (nodata if len(nodata) >= len(flags) else flags).pop()
