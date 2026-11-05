#!/usr/bin/env python3
"""Build scoreboard.json: LMArena, Epoch and two price catalogs joined on our model ids.

OpenRouter's model list is read only as a cross-check: it can raise PRICE-MISMATCH and
EFFORT-MISMATCH flags and break a tie between the two catalogs, but no price, effort level or
default of its own is written to the snapshot (its terms don't license redistribution).

CI only. pyarrow is imported inside the live parquet reader, so tests and fixture builds
run on the standard library. LiveBench contributes only its current release id; its scores
are fetched by the skill on the person's machine and never written here.

    build_scoreboard.py --out PATH [--fixtures DIR] [--record DIR] [--previous PATH] [--today YYYY-MM-DD]

Exit 0 when the snapshot validates, 1 when it does not (the file is still written).
"""
import argparse
import csv
import datetime as dt
import io
import json
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugin" / "skills" / "promptgremlin"
sys.path.insert(0, str(SKILL / "scripts"))

from pglib import fetch, lineup, names, registry  # noqa: E402
from pglib import scoreboard as S  # noqa: E402

ALIASES_PATH = SKILL / "model_aliases.json"
SCHEDULE_PATH = ROOT / "tools" / "price_schedule.json"

ARENA_URL = ("https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset/resolve/main/"
             "{}/latest-00000-of-00001.parquet")
ARENA_INFO = "https://huggingface.co/api/datasets/lmarena-ai/leaderboard-dataset"
ARENA_CONFIGS = ("text", "webdev", "agent", "search", "document",
                 "text_to_image", "image_edit", "text_to_video", "image_to_video")
EPOCH_ZIP = "https://epoch.ai/data/benchmark_data.zip"
EPOCH_ECI = "epoch_capabilities_index/eci_scores.csv"
MODELS_DEV = "https://models.dev/api.json"
LITELLM = "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json"
OPENROUTER = "https://openrouter.ai/api/v1/models"
LIVEBENCH = "https://livebench.ai/"
LIVEBENCH_DATA = "https://livebench.ai/data/"

LICENCES = {"cc-by-4.0": "CC BY 4.0"}
CATALOGS = ("models.dev", "litellm", "openrouter")
# The catalogs whose figures may be published (MIT); OpenRouter only votes and cross-checks.
PUBLISHED_CATALOGS = ("models.dev", "litellm")
# LiteLLM lists every reseller (Bedrock, Azure, Vertex...); these providers are the vendors
# themselves, each counted only for its own family (DashScope and Mistral also host GLM and Kimi).
LITELLM_FIRST_PARTY = {"anthropic": "anthropic", "openai": "openai", "gemini": "gemini", "xai": "xai",
                       "deepseek": "deepseek", "mistral": "mistral", "moonshot": "kimi", "zai": "zhipu",
                       "dashscope": "qwen", "meta_llama": "meta"}
EFFORT_ORDER = ("minimal", "low", "medium", "high", "xhigh", "max")
TOP_N = 30          # board scale reference and the unmapped window
STALE_DAYS = 21
MIN_MAPPED = 20
PRICE_TOLERANCE = 0.10
TIMEOUT = 60


# ---- reading sources (live or recorded) -------------------------------------------------

def _get_bytes(url):
    req = urllib.request.Request(url, headers={"User-Agent": fetch.DEFAULT_UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read()


def _json_source(url, fixture, fixtures):
    if fixtures:
        return json.loads((Path(fixtures) / fixture).read_text(encoding="utf-8"))
    got = fetch.fetch(url, "json", force=True)
    if got.state != "live":
        raise OSError(got.error or got.state)
    return json.loads(got.text)


def arena_rows(config, fixtures=None, get=_get_bytes):
    """Rows of one board's latest split. Recorded fixtures are JSON row lists."""
    if fixtures:
        return json.loads((Path(fixtures) / f"arena_{config}.json").read_text(encoding="utf-8"))
    import pyarrow.parquet as pq   # CI only
    return pq.read_table(io.BytesIO(get(ARENA_URL.format(config)))).to_pylist()


def arena_licence(fixtures=None):
    if fixtures:
        return _meta(fixtures)["lmarena_licence"]
    lic = _json_source(ARENA_INFO, None, None).get("cardData", {}).get("license", "")
    return LICENCES.get(lic, lic or "unknown")


def epoch_input(fixtures=None, get=_get_bytes):
    """(eci_scores.csv text, zip build date, licence read from the README)."""
    if fixtures:
        m = _meta(fixtures)
        return ((Path(fixtures) / "epoch_eci.csv").read_text(encoding="utf-8"),
                m["epoch_zip_built"], m["epoch_licence"])
    z = zipfile.ZipFile(io.BytesIO(get(EPOCH_ZIP)))
    built = max(i.date_time for i in z.infolist())
    readme = z.read("README.md").decode("utf-8", "replace")
    lic = "CC BY 4.0" if "creativecommons.org/licenses/by/4.0" in readme else "unknown"
    return z.read(EPOCH_ECI).decode("utf-8"), dt.date(*built[:3]).isoformat(), lic


def livebench_bundle(fixtures=None, get=_get_bytes):
    if fixtures:
        return (Path(fixtures) / "livebench_bundle.js").read_text(encoding="utf-8")
    page = get(LIVEBENCH).decode("utf-8", "replace")
    m = re.search(r'src="\.?/?(static/js/main\.[0-9a-f]+\.js)"', page)
    if not m:
        raise ValueError("no main bundle in the LiveBench page")
    return get(LIVEBENCH + m.group(1)).decode("utf-8", "replace")


def _meta(fixtures):
    return json.loads((Path(fixtures) / "meta.json").read_text(encoding="utf-8"))


def gather(fixtures=None):
    """Source name -> zero-argument loader. build() calls each and survives a failure."""
    inp = {f"lmarena:{c}": (lambda c=c: arena_rows(c, fixtures)) for c in ARENA_CONFIGS
           if not fixtures or (Path(fixtures) / f"arena_{c}.json").exists()}
    inp["lmarena"] = lambda: arena_licence(fixtures)
    inp["epoch"] = lambda: epoch_input(fixtures)
    inp["models.dev"] = lambda: _json_source(MODELS_DEV, "models_dev.json", fixtures)
    inp["litellm"] = lambda: _json_source(LITELLM, "litellm.json", fixtures)
    inp["openrouter"] = lambda: _json_source(OPENROUTER, "openrouter.json", fixtures)
    inp["livebench"] = lambda: livebench_bundle(fixtures)
    return inp


# ---- per-source parsing (pure) ---------------------------------------------------------

def _main_key(config, category):
    """webdev repeats its overall board as category "webdev"; both are the main board, so
    arena_metrics keeps one row per model name in each key."""
    if category in ("overall", config):
        return f"lmarena:{config}"
    return f"lmarena:{config}/{category}"


def _value(r):
    return r["score"] if "score" in r else r["rating"]


def _round(v, digits=None):
    """None for a blank or missing number: an interval or count can be absent on a new row."""
    try:
        return round(float(v), digits)
    except (TypeError, ValueError):
        return None


def _metric_row(r, effort):
    if "score" in r:
        return {"effort": effort, "score": _round(r["score"], 4),
                "lo": _round(r.get("score_ci_lower"), 4), "hi": _round(r.get("score_ci_upper"), 4)}
    votes = _round(r.get("vote_count"))
    return {"effort": effort, "elo": _round(r["rating"]), "lo": _round(r.get("rating_lower")),
            "hi": _round(r.get("rating_upper")), "votes": votes}


def arena_metrics(config, rows, aliases):
    """(metrics by id, board scales, top-30 (name, rating) pairs that map to nothing, main board's date)."""
    by_key = {}
    for r in rows:
        if _value(r) is not None:
            by_key.setdefault(_main_key(config, r["category"]), {}).setdefault(r["model_name"], r)
    metrics, scales, unmapped = {}, {}, []
    main = f"lmarena:{config}"
    for key, named in by_key.items():
        by_key[key] = rs = sorted(named.values(), key=_value, reverse=True)
        scales[key] = _scale(rs)
        for i, r in enumerate(rs):
            mid = names.canonical("lmarena", r["model_name"], aliases)
            if mid is None:
                if key == main and i < TOP_N and r["model_name"] not in (n for n, _ in unmapped):
                    unmapped.append((r["model_name"], _value(r)))
                continue
            effort = names.split_effort(r["model_name"])[1]
            have = metrics.setdefault(mid, {}).setdefault(key, [])
            if not any(x["effort"] == effort for x in have):
                have.append(_metric_row(r, effort))
    dates = [str(r["leaderboard_publish_date"]) for r in by_key.get(main, [])]
    return metrics, scales, unmapped, max(dates) if dates else None


def _scale(rs):
    top, p30 = _value(rs[0]), _value(rs[min(TOP_N, len(rs)) - 1])
    if "score" in rs[0]:
        return {"top": round(top, 4), "p30": round(p30, 4)}
    return {"top": round(top), "p30": round(p30)}


def livebench_release(bundle_js):
    """Newest v2 release id from the bundle's release array (["20261014","20261025"])."""
    ids = []
    for m in re.finditer(r'\[\s*"\d{8}"(?:\s*,\s*"\d{8}")*\s*\]', bundle_js):
        ids += re.findall(r"\d{8}", m.group(0))
    return max(ids) if ids else None


def epoch_eci(csv_text, aliases):
    out = {}
    for r in csv.DictReader(io.StringIO(csv_text)):
        name = r.get("model_versions") or r["Model"]
        mid = names.canonical("epoch", name, aliases) or names.canonical("epoch", r["Model"], aliases)
        if mid is None or mid in out or _round(r.get("eci"), 2) is None:
            continue
        row = {"score": float(r["eci"]), "lo": _round(r.get("eci_ci_low"), 2),
               "hi": _round(r.get("eci_ci_high"), 2)}
        effort = names.split_effort(name)[1]
        if effort:
            row["effort"] = effort
        out[mid] = row
    return out


def epoch_scale(csv_text):
    """The index's own top and 30th score, so our aliased subset doesn't set the scale."""
    vals = sorted((v for v in (_round(r.get("eci"), 2) for r in csv.DictReader(io.StringIO(csv_text)))
                   if v is not None), reverse=True)
    return {"top": vals[0], "p30": vals[min(TOP_N, len(vals)) - 1]} if vals else None


def _first_party_models_dev(models_dev):
    """models.dev entries listed by the vendor itself (provider key = canonical id prefix)."""
    for pkey, p in (models_dev or {}).items():
        for m in (p.get("models") or {}).values():
            if (m.get("canonical_model_id") or "").split("/")[0] == pkey:
                yield m


def _per_million(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    return round(v * 1e6, 4) if v > 0 else None


def _catalog_prices(models_dev, litellm, openrouter, aliases, first_party):
    out = {}   # id -> {catalog: (in, out)}

    def put(src, name, pin, pout):
        mid = names.canonical(src, name, aliases)
        if mid and pin is not None and pout is not None:
            out.setdefault(mid, {}).setdefault(src, (pin, pout))

    for m in _first_party_models_dev(models_dev):
        c = m.get("cost") or {}
        if c.get("input") is not None and c.get("output") is not None:
            put("models.dev", m["id"], round(float(c["input"]), 4), round(float(c["output"]), 4))
    for key, e in (litellm or {}).items():
        prov = e.get("litellm_provider") if isinstance(e, dict) else None
        prefix = key.split("/")[0] if "/" in key else None
        mid = names.canonical("litellm", key, aliases) if prov in first_party else None
        if mid and aliases[mid].get("family") == first_party[prov] and prefix in (None, prov) \
                and key.count("/") <= 1:
            put("litellm", key, _per_million(e.get("input_cost_per_token")),
                _per_million(e.get("output_cost_per_token")))
    for e in (openrouter or {}).get("data", []):
        p = e.get("pricing") or {}
        put("openrouter", e["id"], _per_million(p.get("prompt")), _per_million(p.get("completion")))
    return out


def _agree(a, b):
    return all(abs(x - y) <= PRICE_TOLERANCE * max(x, y) for x, y in zip(a, b))


def prices(models_dev, litellm, openrouter, aliases, schedule, today, first_party=LITELLM_FIRST_PARTY):
    """USD per million tokens. A value two catalogs agree on, else models.dev's, else LiteLLM's;
    scheduled prices win. The value is always a published catalog's own figure: OpenRouter only
    breaks a tie and raises PRICE-MISMATCH, so a model only it prices gets no price."""
    found = _catalog_prices(models_dev, litellm, openrouter, aliases, first_party)
    price, flags = {}, []
    for mid in aliases:
        cats = [(c, found[mid][c]) for c in CATALOGS if c in found.get(mid, {})]
        if cats:
            pairs = [(a, b) for i, a in enumerate(cats) for b in cats[i + 1:] if _agree(a[1], b[1])]
            # CATALOGS order puts OpenRouter last, so the first of a pair is a published one.
            if pairs:
                val, src = pairs[0][0][1], "majority"
            else:
                val, src = cats[0][1], cats[0][0]
            if len(cats) > 1 and not all(_agree(val, v) for _, v in cats):
                flags.append(f"PRICE-MISMATCH {mid}")
            if cats[0][0] in PUBLISHED_CATALOGS:
                price[mid] = {"in": val[0], "out": val[1], "from": src}
        for s in sorted((s for s in schedule if s["model"] == mid), key=lambda s: s["from"]):
            if dt.date.fromisoformat(s["from"]) <= today:
                price[mid] = {"in": s["in"], "out": s["out"], "from": f"schedule {s['from']}"}
            else:
                flags.append(f"PRICE-CHANGE {mid} {s['from']}")
    return price, flags


def _ordered(levels):
    return [e for e in EFFORT_ORDER if e in levels]


def efforts(models_dev, aliases):
    """Effort levels from models.dev. The starting level comes from each family's notes, on the
    person's machine."""
    out = {}
    for m in _first_party_models_dev(models_dev):
        mid = names.canonical("models.dev", m["id"], aliases)
        for opt in m.get("reasoning_options") or []:
            if mid and opt.get("type") == "effort" and mid not in out and _ordered(opt.get("values", [])):
                out[mid] = {"levels": _ordered(opt.get("values", []))}
    return out


def openrouter_defaults(openrouter, aliases):
    """{id: OpenRouter's default effort}, for the EFFORT-MISMATCH cross-check only."""
    out = {}
    for e in (openrouter or {}).get("data", []):
        mid = names.canonical("openrouter", e["id"], aliases)
        level = (e.get("reasoning") or {}).get("default_effort")
        if mid and mid not in out and level in EFFORT_ORDER:
            out[mid] = level
    return out


def effort_flags(models, defaults, skill=SKILL):
    """EFFORT-MISMATCH for each model whose notes start at another level than OpenRouter's
    default: the skill's own notes reader, run on a throwaway copy that holds the defaults."""
    tmp = {"models": {mid: {"name": m.get("name", mid), "efforts": {"default": defaults[mid],
                                                                     "default_from": "openrouter"}}
                      for mid, m in models.items() if mid in defaults}}
    reg = registry.load(Path(skill) / "sources.json")
    return S.add_note_efforts(tmp, reg, Path(skill) / "targets").get("flags", [])


# ---- assembly --------------------------------------------------------------------------

def _carry_arena(previous, models, boards, config):
    key = f"lmarena:{config}"
    hit = lambda k: k == key or k.startswith(key + "/")  # noqa: E731
    for mid, m in models.items():
        for k, v in previous.get("models", {}).get(mid, {}).get("metrics", {}).items():
            if hit(k):
                m["metrics"][k] = v
    boards.update({k: v for k, v in previous.get("boards", {}).items() if hit(k)})
    return previous.get("sources", {}).get("lmarena", {}).get("published", {}).get(config)


def _stale(source, date, today):
    if date and (today - dt.date.fromisoformat(date)).days > STALE_DAYS:
        return [f"SOURCE-STALE {source} {date}"]
    return []


def _try(name, flags, fn, *args):
    """fn(*args), or None and SOURCE-FAIL when a source can't be fetched or parsed."""
    try:
        return fn(*args)
    except Exception as e:
        print(f"{name}: {type(e).__name__}: {e}"[:300], file=sys.stderr)
        flags.append(f"SOURCE-FAIL {name}")
        return None


def build(inputs, aliases, schedule, today, previous=None):
    previous = previous or {}
    prev_models = previous.get("models", {})
    prev_sources = previous.get("sources", {})
    got, flags = {}, []
    for name, load in inputs.items():
        value = _try(name, flags, load)
        if value is not None:
            got[name] = value

    models = {mid: {"family": e["family"], "name": mid, "metrics": {}} for mid, e in aliases.items()}
    boards, published = {}, {}
    for config in ARENA_CONFIGS:
        key = f"lmarena:{config}"
        parsed = _try(key, flags, arena_metrics, config, got[key], aliases) if key in got else None
        if parsed:
            metrics, scales, unmapped, date = parsed
            for mid, ms in metrics.items():
                models[mid]["metrics"].update(ms)
            boards.update(scales)
            # The rating rides along so --suggest can show only names that beat its pick.
            flags += [f"UNMAPPED {key} {n} @{v:.4g}" for n, v in unmapped]
        elif key in inputs:
            date = _carry_arena(previous, models, boards, config)
        else:
            continue
        published[config] = date
        flags += _stale(key, date, today)

    epoch = dict(prev_sources.get("epoch", {}))
    parse = lambda text: (epoch_eci(text, aliases), epoch_scale(text))  # noqa: E731
    eci = _try("epoch", flags, parse, got["epoch"][0]) if "epoch" in got else None
    if eci is not None:
        epoch = {"licence": got["epoch"][2], "zip_built": got["epoch"][1]}
        for mid, row in eci[0].items():
            models[mid]["metrics"]["epoch:eci"] = row
        if eci[1]:
            boards["epoch:eci"] = eci[1]
    else:
        if "epoch:eci" in previous.get("boards", {}):
            boards["epoch:eci"] = previous["boards"]["epoch:eci"]
        for mid, m in models.items():
            if "epoch:eci" in prev_models.get(mid, {}).get("metrics", {}):
                m["metrics"]["epoch:eci"] = prev_models[mid]["metrics"]["epoch:eci"]
    flags += _stale("epoch", epoch.get("zip_built"), today)

    price, pflags = prices(got.get("models.dev"), got.get("litellm"), got.get("openrouter"),
                           aliases, schedule, today)
    flags += pflags
    eff = efforts(got.get("models.dev"), aliases)
    display = _display_names(got.get("models.dev"), aliases)
    for mid, m in models.items():
        prev = prev_models.get(mid, {})
        # A previous snapshot may predate the cross-check-only rule: carry only published figures.
        prev_price = prev.get("price") if (prev.get("price") or {}).get("from") != "openrouter" else None
        if mid in price or prev_price:
            m["price"] = price.get(mid, prev_price)
        # Older snapshots marked efforts default_from openrouter, and their levels may be its too.
        pe = prev.get("efforts") or {}
        prev_eff = {"levels": pe["levels"]} if pe.get("levels") and "default_from" not in pe else None
        if mid in eff or prev_eff:
            m["efforts"] = eff.get(mid, prev_eff)
        m["name"] = display.get(mid) or prev.get("name") or mid
    if "openrouter" in got:
        flags += effort_flags(models, openrouter_defaults(got["openrouter"], aliases))

    release = livebench_release(got["livebench"]) if "livebench" in got else None
    if release is None and "livebench" in got:
        flags.append("SOURCE-FAIL livebench")
    release = release or prev_sources.get("livebench", {}).get("release")

    lic = got.get("lmarena") or prev_sources.get("lmarena", {}).get("licence")
    fetched = today.isoformat() if "openrouter" in got else prev_sources.get("openrouter", {}).get("fetched")
    return {
        "version": 1,
        "built_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sources": {
            "lmarena": {"licence": lic, "published": published},
            "epoch": epoch,
            "models.dev": {"licence": "MIT"},
            "litellm": {"licence": "MIT"},
            "openrouter": {"fetched": fetched},
            "livebench": {"release": release, "base": LIVEBENCH_DATA},
        },
        "boards": boards,
        "models": models,
        "flags": list(dict.fromkeys(flags)),
    }


def _display_names(models_dev, aliases):
    out = {}
    for m in _first_party_models_dev(models_dev):
        mid = names.canonical("models.dev", m["id"], aliases)
        if mid and m.get("name"):
            out.setdefault(mid, m["name"])
    return out


def validate(snapshot, notes_flagships, previous=None):
    errs = []
    for k in ("version", "built_at", "sources", "boards", "models", "flags"):
        if k not in snapshot:
            errs.append(f"missing {k}")
    if errs:
        return errs
    models, src = snapshot["models"], snapshot["sources"]
    for mid, m in models.items():
        if not m.get("family") or not isinstance(m.get("metrics"), dict):
            errs.append(f"{mid}: needs family and metrics")
    for board in ("lmarena:text", "lmarena:webdev"):
        n = sum(1 for m in models.values() if board in m.get("metrics", {}))
        if n < MIN_MAPPED:
            errs.append(f"{board}: {n} mapped models, need {MIN_MAPPED}")
    published = src.get("lmarena", {}).get("published", {})
    for c in ARENA_CONFIGS:
        if not published.get(c):
            errs.append(f"no publish date for lmarena:{c}")
    for path, val in (("epoch.zip_built", src.get("epoch", {}).get("zip_built")),
                      ("openrouter.fetched", src.get("openrouter", {}).get("fetched")),
                      ("livebench.release", src.get("livebench", {}).get("release"))):
        if not val:
            errs.append(f"no {path}")
    for fam, mid in notes_flagships.items():
        if not any(k.startswith("lmarena:") for k in models.get(mid, {}).get("metrics", {})):
            errs.append(f"{fam} flagship {mid} has no Arena row")
    for name, s in (previous or {}).get("sources", {}).items():
        was, now = s.get("licence"), src.get(name, {}).get("licence")
        if was and was != now:
            errs.append(f"{name} licence changed: {was} -> {now}")
    return errs


def family_note_ids():
    reg = registry.load(SKILL / "sources.json")
    ids = registry.note_ids_by_key(SKILL / "targets", reg)
    return {k: ids[k] for k, e in reg.items() if e.get("kind") == "family"}


def notes_flagships():
    reg = registry.load(SKILL / "sources.json")
    out = {}
    for key, ids in family_note_ids().items():
        lu = reg[key].get("lineup") or {}
        lu = lu[0] if isinstance(lu, list) else lu
        if ids:
            out[key] = lineup.flagship(ids, lu)
    return out


# ---- recording fixtures ----------------------------------------------------------------

ARENA_KEEP = {"overall", "webdev", "coding", "creative_writing"}
UNMAPPED_KEEP = 5


def _interest(aliases):
    """Our aliases plus every family note id, so later alias work has rows to map."""
    out = dict(aliases)
    for key, ids in family_note_ids().items():
        for mid in ids:
            out.setdefault(mid, {"family": key})
    return out


def _trim_arena(config, rows, interest):
    main = sorted((r for r in rows if r["category"] in ("overall", config)), key=_value, reverse=True)
    top = set(list(dict.fromkeys(r["model_name"] for r in main))[:TOP_N])
    drop = ("organization", "license", "variance", "rank", "observation_count", "session_count")
    keep = []
    for r in rows:
        if r["model_name"] in top and r["category"] in ("overall", config) or (
                r["category"] in ARENA_KEEP and names.canonical("lmarena", r["model_name"], interest)):
            keep.append({k: _short(k, v) for k, v in r.items() if k not in drop})
    return keep


def _short(k, v):
    if k == "leaderboard_publish_date":
        return str(v)
    if isinstance(v, float):
        return round(v, 2) if abs(v) >= 10 else round(v, 4)
    return v


def _trim_epoch(text, interest):
    lines = text.splitlines()
    keep = [lines[0]] + lines[1:TOP_N + 1]
    for line, r in zip(lines[1:], csv.DictReader(io.StringIO(text))):
        if line not in keep and names.canonical("epoch", r["Model"], interest):
            keep.append(line)
    return "\n".join(keep) + "\n"


def _trim_models_dev(md, interest):
    out, others = {}, 0
    for pkey, p in md.items():
        for m in (p.get("models") or {}).values():
            if (m.get("canonical_model_id") or "").split("/")[0] != pkey:
                continue
            mapped = names.canonical("models.dev", m["id"], interest)
            if not mapped and others >= UNMAPPED_KEEP:
                continue
            others += not mapped
            slim = {k: m[k] for k in ("id", "name", "reasoning_options", "canonical_model_id") if k in m}
            slim["cost"] = {k: (m.get("cost") or {}).get(k) for k in ("input", "output")}
            out.setdefault(pkey, {"id": pkey, "models": {}})["models"][m["id"]] = slim
    return out


def _trim_litellm(ll, interest):
    fields = ("litellm_provider", "input_cost_per_token", "output_cost_per_token", "mode")
    out = {}
    for key, e in ll.items():
        if isinstance(e, dict) and names.canonical("litellm", key, interest) and key.count("/") <= 1:
            if e.get("litellm_provider") in LITELLM_FIRST_PARTY or key.startswith(("azure/", "bedrock/")):
                out[key] = {k: e[k] for k in fields if k in e}
    return out


def _trim_openrouter(orr, interest):
    data, others = [], 0
    for e in orr.get("data", []):
        mapped = names.canonical("openrouter", e["id"], interest)
        if not mapped and others >= UNMAPPED_KEEP:
            continue
        others += not mapped
        data.append({"id": e["id"], "name": e.get("name"),
                     "pricing": {k: e.get("pricing", {}).get(k) for k in ("prompt", "completion")},
                     "reasoning": e.get("reasoning")})
    return {"data": data}


def _trim_bundle(js):
    """A hand-shaped line holding only the release ids, so no LiveBench code is saved."""
    ids = re.findall(r"\d{8}", "".join(re.findall(r'\[\s*"\d{8}"(?:\s*,\s*"\d{8}")*\s*\]', js)))
    return f"const releases = [{', '.join(chr(34) + i + chr(34) for i in ids)}];\n" if ids else ""


def record(got, out_dir, aliases, today):
    """Write trimmed copies of live responses as test fixtures. No LiveBench CSV is saved."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    interest = _interest(aliases)

    def dump(name, obj):
        (out / name).write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":"), default=str)
                                .replace("},{", "},\n{") + "\n", encoding="utf-8")

    for c in ARENA_CONFIGS:
        if f"lmarena:{c}" in got:
            dump(f"arena_{c}.json", _trim_arena(c, got[f"lmarena:{c}"], interest))
    text, built, lic = got["epoch"]
    (out / "epoch_eci.csv").write_text(_trim_epoch(text, interest), encoding="utf-8")
    dump("models_dev.json", _trim_models_dev(got["models.dev"], interest))
    dump("litellm.json", _trim_litellm(got["litellm"], interest))
    dump("openrouter.json", _trim_openrouter(got["openrouter"], interest))
    (out / "livebench_bundle.js").write_text(_trim_bundle(got["livebench"]), encoding="utf-8")
    (out / "meta.json").write_text(json.dumps({
        "recorded": today.isoformat(), "lmarena_licence": got["lmarena"],
        "epoch_zip_built": built, "epoch_licence": lic}, indent=1) + "\n", encoding="utf-8")


# ---- CLI -------------------------------------------------------------------------------

FLAT = re.compile(r"\{\n\s*([^{}\[\]]*?)\n\s*\}")
ROWS = re.compile(r"\[\n\s*(\{[^{}\[\]]*\}(?:,\n\s*\{[^{}\[\]]*\})*)\n\s*\]")


def dumps(snap):
    """Indented JSON with each metric on one line: small, and a readable daily diff."""
    text = json.dumps(snap, indent=1, ensure_ascii=False)
    text = FLAT.sub(lambda m: "{" + re.sub(r",\n\s*", ", ", m.group(1)) + "}", text)
    return ROWS.sub(lambda m: "[" + re.sub(r",\n\s*", ", ", m.group(1)) + "]", text) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", required=True)
    ap.add_argument("--fixtures")
    ap.add_argument("--record")
    ap.add_argument("--previous")
    ap.add_argument("--today")
    a = ap.parse_args(argv)
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    aliases = json.loads(Path(ALIASES_PATH).read_text(encoding="utf-8"))
    schedule = json.loads(Path(SCHEDULE_PATH).read_text(encoding="utf-8"))
    previous = None
    if a.previous and Path(a.previous).exists():
        previous = json.loads(Path(a.previous).read_text(encoding="utf-8"))

    inputs = gather(a.fixtures)
    if a.record:
        got = {}
        for name, load in inputs.items():
            got[name] = load()   # recording needs every source; let a failure stop it
        record(got, a.record, aliases, today)
        inputs = {name: (lambda v=v: v) for name, v in got.items()}

    snap = build(inputs, aliases, schedule, today, previous)
    text = dumps(snap)
    Path(a.out).write_text(text, encoding="utf-8")
    errs = validate(snap, notes_flagships(), previous)
    print(f"wrote {a.out} ({len(text.encode()) // 1024} KB, {len(snap['models'])} models)")
    for f in snap["flags"]:
        print(f"flag: {f}")
    for e in errs:
        print(f"invalid: {e}", file=sys.stderr)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
