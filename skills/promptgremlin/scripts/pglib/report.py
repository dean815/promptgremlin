"""Build the per-target briefing, the all-targets freshness report, and refresh output."""
import datetime as dt
from pathlib import Path
from typing import NamedTuple

from . import fetch as F
from . import lineup as L
from . import notes as N
from . import registry as R
from . import sections as S

CHANGED_CAP = 1500   # per changed section, at most
OUTPUT_BUDGET = 7400  # whole per-target briefing; changed sections shrink to fit
MIN_CHANGED = 300


class Ctx(NamedTuple):
    reg: dict
    reg_path: Path
    notes_dir: Path
    offline: bool
    today: dt.date
    now: dt.datetime
    force: bool = False  # bypass the 24h cache (refresh reads and fingerprints live text)


class Collected(NamedTuple):
    parts: list
    flags: list
    changed: list
    states: list
    chosen: object
    flagship: object


def _get(url, fmt, ctx):
    return F.fetch(url, fmt, offline=ctx.offline, now=ctx.now, force=ctx.force)


def _wrap_vendor_text(source, body):
    """Fence fetched vendor text so the reader treats it as data. The fence can't be forged from inside."""
    body = body.replace("<<<", "< < <").replace(">>>", "> > >")
    source = source.replace('"', "'").replace("<<<", "").replace(">>>", "")
    return f'<<<vendor-text source="{source}">>>\n{body}\n<<<end vendor-text>>>'


def _lineup(entry, ctx):
    """(models, flagship, Fetched or None when the entry has no lineup)."""
    return _lineup_full(entry, ctx)[:3]


def _lineup_full(entry, ctx):
    """_lineup plus a 4th item: True when any spec loaded text but parsed to no models.


    entry["lineup"] may be one spec or a list of specs. Models from every spec that loaded are
    concatenated in order and de-duplicated; the flagship comes from the first spec that yields
    one. The returned Fetched is aggregate: text is None only when no spec loaded, and error is
    set when any spec failed to load cleanly (so callers still raise FETCH-FAIL).
    """
    specs = entry.get("lineup")
    if not specs:
        return [], None, None, False
    if isinstance(specs, dict):
        specs = [specs]
    models, flagship, fetched, empty = [], None, [], False
    for spec in specs:
        f = _get(spec["url"], spec["format"], ctx)
        fetched.append(f)
        if f.text is None:
            continue
        found = L.parse(f.text, spec)
        empty = empty or not found
        flagship = flagship or L.flagship(found, spec)
        models += [m for m in found if m not in models]
    if len(fetched) == 1:
        return models, flagship, fetched[0], empty
    loaded = [f for f in fetched if f.text is not None]
    errors = [f.error for f in fetched if f.error or f.text is None]
    states = {f.state for f in loaded}
    agg = F.Fetched(
        "\n".join(f.text for f in loaded) if loaded else None,
        "cache" if "cache" in states else ("live" if loaded else "missing"),
        min((f.date for f in loaded), default=None),
        "; ".join(e or "no text" for e in errors) or None)
    return models, flagship, agg, empty


def _source_urls(name, src, model_ids):
    """[(fingerprint key, url)]; url_pattern sources expand once per model."""
    if src.get("format") == "none":
        return []
    if "url" in src:
        return [(name, src["url"])]
    return [(f"{name}:{m}", src["url_pattern"].format(model=m)) for m in model_ids]


def _suspect_parse(models, note_ids):
    """True if models is non-empty, >= 2 notes, and would retire > 50% of notes."""
    if not models or len(note_ids) < 2:
        return False
    retired_count = sum(1 for m in note_ids if m not in models)
    return retired_count > len(note_ids) / 2


def _collect(key, model, ctx, expand_all=False):
    entry = ctx.reg[key]
    notes_path = ctx.notes_dir / f"{key}.md"
    if not notes_path.exists():
        return Collected([], [f"NO NOTES {key}"], [], [], None, None)
    notes = N.load(notes_path)
    note_ids = N.model_ids(notes)
    flags, changed, states = [], [], []

    models, flagship, lf, empty = _lineup_full(entry, ctx)
    if empty:
        flags.append(f"FETCH-FAIL {key} lineup (empty parse)")
    if lf is not None:
        if lf.text is not None:
            states.append(lf)
        # Flag FETCH-FAIL if online and (no text or error occurred)
        if not ctx.offline and (lf.text is None or lf.error):
            flags.append(f"FETCH-FAIL {key} lineup")

    retired = []
    if models:
        # Check for suspect parse
        if _suspect_parse(models, note_ids):
            matched = sum(1 for m in note_ids if m in models)
            flags.append(f"FETCH-FAIL {key} lineup (suspect parse: matched {matched} of {len(note_ids)} noted models)")
            retired = []  # Don't retire on suspect parse
        else:
            new, retired = L.compare(models, note_ids)
            flags += [f"NEW MODEL {m}" for m in new] + [f"RETIRED {m}" for m in retired]

    chosen = None
    if note_ids or models:
        if model:
            q = L.norm_id(model)
            chosen = L.match_model(q, list(dict.fromkeys(models + note_ids))) or q
            if chosen not in models and chosen not in note_ids:
                flags.append(f"UNKNOWN MODEL {chosen}")
        else:
            chosen = flagship or next((m for m in note_ids if m not in retired), None)

    # url_pattern pages: just the chosen model for a briefing; every live noted model plus the
    # flagship for a freshness check.
    page_models = [chosen] if chosen else []
    if expand_all:
        page_models = list(dict.fromkeys(page_models + [m for m in note_ids if m not in retired]))
    stored_fps = entry.get("fingerprints", {})

    live_ok, all_none = False, True
    for name, src in entry.get("sources", {}).items():
        if src.get("format") != "none":
            all_none = False
        for fp_key, url in _source_urls(name, src, page_models):
            f = _get(url, src["format"], ctx)
            # An optional source may fail silently only until it has been fingerprinted.
            quiet = src.get("optional") and fp_key not in stored_fps
            if f.text is None:
                if not ctx.offline and not quiet:
                    flags.append(f"FETCH-FAIL {fp_key}")
                continue
            # Flag cache fallback errors even when text is present
            if f.error and not ctx.offline and not quiet:
                flags.append(f"FETCH-FAIL {fp_key}")
            states.append(f)
            if f.state == "live" and not src.get("optional"):
                live_ok = True
            if "url_pattern" in src and fp_key not in stored_fps:
                # notes for this model were never verified against its page; one flag, no dump
                flags.append(f"DRIFT unfingerprinted {fp_key}")
                continue
            fp = stored_fps.get(fp_key, {})
            for kind, detail, body in S.drift(fp_key, f.text, src.get("watch", ["##"]), fp):
                if kind == "changed":
                    flags.append(f"DRIFT {detail}")
                    changed.append((detail, body))
                else:
                    flags.append(f"DRIFT {kind} {detail}")

    if all_none or (N.is_stale(notes, ctx.today) and not live_ok):
        flags.append(f"STALE {key} (last verified {notes.meta.get('last_verified', 'never')})")

    parts = [f"## {key}: All models\n\n{notes.blocks.get('All models', '(no notes)')}"]
    if chosen and chosen in notes.blocks and chosen not in retired:
        parts.append(f"## {chosen}\n\n{notes.blocks[chosen]}")
    if "Effort" in notes.blocks:
        parts.append(f"## {key}: Effort\n\n{notes.blocks['Effort']}")
    for used in entry.get("uses", []):
        sub = _collect(used, model, ctx, expand_all)
        parts += sub.parts
        flags += sub.flags
        changed += sub.changed
        states += sub.states
        chosen = chosen or sub.chosen
        flagship = flagship or sub.flagship
    return Collected(parts, flags, changed, states, chosen, flagship)


def _state_summary(states):
    """Report worst state: cache (oldest date) < live (newest date) < notes-only."""
    cache = [s.date for s in states if s.state == "cache"]
    if cache:
        return f"cache {min(cache)}"
    live = [s.date for s in states if s.state == "live"]
    if live:
        return f"live {max(live)}"
    return "notes-only"


def target_report(key, model, ctx):
    c = _collect(key, model, ctx)
    lines = [f"<!-- promptgremlin | target={key} | model={c.chosen or '-'} | "
             f"flagship={c.flagship or '-'} | {_state_summary(c.states)} -->"]
    if c.flags:
        lines.append("FLAGS: " + "; ".join(c.flags))
    lines += c.parts
    if c.changed:
        lines.append("## Changed since notes were written")
        used = len("\n\n".join(lines)) + sum(130 + 2 * len(d) for d, _ in c.changed)   # headings and delimiters
        used += 100   # slack for the truncation note
        cap = max(MIN_CHANGED, min(CHANGED_CAP, (OUTPUT_BUDGET - used) // len(c.changed)))
        lines += [f"### {d}\n\n{_wrap_vendor_text(d, S.cap(S.clean(b), cap))}" for d, b in c.changed]
    return "\n\n".join(lines), c.flags


def check_all(ctx):
    lines, total = [], 0
    for key in sorted(ctx.reg):
        if not (ctx.notes_dir / f"{key}.md").exists():
            lines.append(f"{key}: NO NOTES")
            total += 1
            continue
        try:
            c = _collect(key, None, ctx, expand_all=True)
        except Exception as e:  # one broken target must not hide the others
            lines.append(f"{key}: ERROR {type(e).__name__}: {e}")
            total += 1
            continue
        lines.append(f"{key}: " + ("; ".join(c.flags) if c.flags else "OK"))
        total += len(c.flags)
    return "\n".join(lines), total


def lineup_report(ctx):
    lines = []
    for key in sorted(ctx.reg):
        entry = ctx.reg[key]
        if not entry.get("lineup"):
            continue
        models, flagship, f, empty = _lineup_full(entry, ctx)
        if f is not None and f.text is None:
            lines.append(f"{key}: (lineup unavailable: {f.error})")
        else:
            note = f" [partial: {f.error}]" if f is not None and f.error else ""
            if empty:
                note += " (empty parse)"
            lines.append(f"{key}: flagship={flagship or '-'} | {', '.join(models) or '(no matches)'}{note}")
    return "\n".join(lines)


def refresh(key, ctx, commit=False):
    ctx = ctx._replace(force=True)  # notes and fingerprints must come from the live page, never a cached copy
    entry = ctx.reg[key]
    path = ctx.notes_dir / f"{key}.md"
    notes = N.load(path) if path.exists() else None
    note_ids = N.model_ids(notes) if notes else []
    models, flagship, lf, empty = _lineup_full(entry, ctx)

    # Check lineup validity for commit
    if commit and lf and lf.error:
        raise SystemExit(f"promptgremlin: --commit needs every source live; not live: {key} lineup")
    if commit and ctx.offline:
        raise SystemExit(f"promptgremlin: --commit needs every source live; not live: {key} (offline)")

    if commit and empty:
        raise SystemExit(f"promptgremlin: --commit needs every source live; empty lineup parse: {key}")

    # Check for suspect parse before retiring
    suspect = _suspect_parse(models, note_ids)
    if commit and suspect:
        matched = sum(1 for m in note_ids if m in models)
        raise SystemExit(f"promptgremlin: --commit needs every source live; suspect parse: matched {matched} of {len(note_ids)} noted models")

    if suspect:
        retired = []
        keep = [m for m in note_ids] if notes else models
        out = [f"# refresh {key}", f"lineup: {', '.join(models) or '(none)'}",
               f"flagship: {flagship or '-'}", f"retired: -"]
        matched = sum(1 for m in note_ids if m in models)
        out.append(f"FETCH-FAIL {key} lineup (suspect parse: matched {matched} of {len(note_ids)} noted models)")
    else:
        retired = [m for m in note_ids if models and m not in models]
        keep = [m for m in note_ids if m not in retired] if notes else models
        out = [f"# refresh {key}", f"lineup: {', '.join(models) or '(none)'}",
               f"flagship: {flagship or '-'}", f"retired: {', '.join(retired) or '-'}"]
    if empty:
        out.append(f"FETCH-FAIL {key} lineup (empty parse)")
    fps = {}
    not_live_sources = []
    for name, src in entry.get("sources", {}).items():
        for fp_key, url in _source_urls(name, src, keep):
            f = _get(url, src["format"], ctx)
            if f.text is None:
                out.append(f"## {fp_key}: UNAVAILABLE ({f.error or 'offline, no cache'})")
                if commit and not src.get("optional"):
                    not_live_sources.append(fp_key)
                continue
            # Check if source is live for commit
            if commit and (f.error or f.state != "live") and not src.get("optional"):
                not_live_sources.append(fp_key)
            found, missing, heads = S.watched(f.text, src.get("watch", ["##"]))
            out.append(f"## {fp_key} ({url}, {len(f.text)} chars, {f.state} {f.date})")
            out.append("headings: " + (" | ".join(heads) or "(none)"))
            if missing:
                out.append("MISSING watched headings: " + ", ".join(missing))
            out += [f"### {t}\n\n{S.clean(b)}" for t, b in found.items()]
            fps[fp_key] = {"sections": {t: S.fingerprint(b) for t, b in found.items()},
                           "headings": heads}

    if commit:
        if notes is None:
            raise SystemExit(f"promptgremlin: write targets/{key}.md before --commit")
        if not_live_sources:
            raise SystemExit(f"promptgremlin: --commit needs every source live; not live: {', '.join(not_live_sources)}")
        merged = {**entry.get("fingerprints", {}), **fps}
        entry["fingerprints"] = {k: v for k, v in merged.items()
                                 if not any(k.endswith(":" + m) for m in retired)}
        R.save(ctx.reg, ctx.reg_path)
        notes, removed = N.remove_blocks(notes, retired)
        if removed:
            arch = ctx.notes_dir / "_archive" / f"{key}.md"
            arch.parent.mkdir(exist_ok=True)
            with arch.open("a", encoding="utf-8") as fh:
                for t, b in removed.items():
                    fh.write(f"## {t} (retired {ctx.today.isoformat()})\n{b}\n\n")
        N.save(N.set_last_verified(notes, ctx.today.isoformat()), path)
        out.append(f"COMMITTED {len(fps)} fingerprint set(s); last_verified={ctx.today.isoformat()}")
    return "\n\n".join(out)
