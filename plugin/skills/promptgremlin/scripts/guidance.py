#!/usr/bin/env python3
"""Current prompting guidance for one target, with freshness flags.

    guidance.py --target <name> [--model <id>] [--offline]
    guidance.py --lineup [--offline]
    guidance.py --check-all [--offline]
    guidance.py --refresh <target> [--commit] [--offline]
    guidance.py --suggest --type <type> [--target <name>] [--session-model <id>]
                [--run-length short|long] [--language <lang>] [--style <style>]
                [--input text|image]
                [--surface api|plan|tool] [--offline]

<name> may be a target key, an alias (chatgpt, claude), or a model (opus 5.5).
--suggest without --target compares every vendor (pool all).
Exit: 0 ok; 1 --check-all found flags; 2 unknown target or type, no notes, or no snapshot.
"""
import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pglib import livebench  # noqa: E402
from pglib import registry as R  # noqa: E402
from pglib import report  # noqa: E402
from pglib import scoreboard as S  # noqa: E402

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG = Path.home() / ".config" / "promptgremlin" / "config.json"


def make_ctx(offline):
    reg_path = SKILL_DIR / "sources.json"
    return report.Ctx(reg=R.load(reg_path), reg_path=reg_path, notes_dir=SKILL_DIR / "targets",
                      offline=offline, today=dt.date.today(), now=dt.datetime.now())


def _read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _config():
    c = _read_json(CONFIG)
    return c if isinstance(c, dict) else {}


def offline_reason(flag):
    """Why this run makes no requests, or None: --offline, PROMPTGREMLIN_OFFLINE=1, or the
    config's "offline": true. Any one of them covers every mode, --suggest included."""
    if flag:
        return "--offline"
    if _on(os.environ.get("PROMPTGREMLIN_OFFLINE")):
        return "PROMPTGREMLIN_OFFLINE"
    if _on(_config().get("offline")):
        return "config offline"
    return None


def _on(value):
    """true, 1, or the strings "1", "true", "yes", "on" in any case: a hand-edited config often
    quotes its booleans."""
    if value is True or (type(value) is int and value == 1):
        return True
    return isinstance(value, str) and value.strip().lower() in ("1", "true", "yes", "on")


OFFLINE_LINE = "offline: cache and bundled data only, no network requests"


def suggest(a, ctx):
    types = sorted(p.stem for p in (SKILL_DIR / "types").glob("*.md"))
    evidence = _read_json(SKILL_DIR / "evidence.json")
    if a.type not in types:
        print(f"promptgremlin: unknown type '{a.type}'. Known: {', '.join(types)}", file=sys.stderr)
        return 2
    if a.type not in evidence:
        print(f"promptgremlin: no evidence for type '{a.type}' in evidence.json", file=sys.stderr)
        return 2
    key, ids = None, R.note_ids_by_key(ctx.notes_dir, ctx.reg)
    # A chat model doesn't make images or video, so the session line would only say "no data".
    session = None if a.type in S.MEDIA_TOOLS else a.session_model
    if a.target:
        try:
            key, _ = R.resolve(a.target, ctx.reg, ids)
        except KeyError:
            print(f"promptgremlin: unknown target '{a.target}'. Known: {', '.join(sorted(ctx.reg))}",
                  file=sys.stderr)
            return 2
    loaded = S.load_snapshot(SKILL_DIR, a.offline, ctx.now)
    if loaded.snapshot is None:
        print("promptgremlin: no scoreboard snapshot, live or bundled", file=sys.stderr)
        return 2
    try:
        text = _suggest_block(a, ctx, loaded, evidence, key, session)
    except Exception:
        # A fetched or cached snapshot that passed the shape checks yet still breaks the
        # suggestion gives way to the bundled one; a broken bundled copy is a real bug.
        if loaded.state == "bundled":
            raise
        loaded = S.load_bundled(SKILL_DIR)
        if loaded.snapshot is None:
            raise
        text = _suggest_block(a, ctx, loaded, evidence, key, session)
    print(text)
    return 0


def _suggest_block(a, ctx, loaded, evidence, key, session):
    snap, state, date = loaded
    lb_src = snap.get("sources", {}).get("livebench", {})
    # The fetched snapshot never picks the URL: the host is fixed in livebench.py, and a release
    # that isn't eight digits gives way to the bundled snapshot's.
    bundled = _read_json(SKILL_DIR / "scoreboard.json").get("sources", {}).get("livebench", {})
    release = livebench.pick_release(lb_src.get("release"), bundled.get("release"))
    lb = livebench.load(release, _read_json(SKILL_DIR / "model_aliases.json"), a.offline, ctx.now)
    snap = S.add_livebench(snap, lb.metrics)
    snap = S.add_note_efforts(snap, ctx.reg, ctx.notes_dir)
    if session:
        # The host names its model its own way ("Claude Opus 5.5 1m"); compare on the snapshot id.
        session = S.session_id(session, snap)
    slots = {k: v.lower() for k, v in (("run_length", a.run_length), ("language", a.language),
                                         ("style", a.style), ("input", a.input)) if v}
    if "style" in slots:
        slots["style"] = S.style_slot(slots["style"], evidence[a.type])
    ev = S.resolve_evidence(evidence, a.type, slots)
    pool = "target" if key else "all"
    cands = S.candidates(key, ctx.reg, ctx.notes_dir, pool, a.type)
    others = S.candidates(None, ctx.reg, ctx.notes_dir, "all", a.type) if key else []
    info = S.Info(a.type, pool, date, state, {"release": release, "state": lb.state}, key, a.offline)
    s = S.choose(cands, snap, ev, info, session=session, others=others)
    priority = _config().get("model_priority", "quality")
    return S.render(s, a.surface, priority)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target")
    ap.add_argument("--model")
    ap.add_argument("--offline", action="store_true",
                    help="cache and bundled data only, no network; PROMPTGREMLIN_OFFLINE=1 or the "
                         "config's \"offline\": true does the same for every run")
    ap.add_argument("--lineup", action="store_true", help="print every family's current models")
    ap.add_argument("--check-all", action="store_true", help="freshness report for every target")
    ap.add_argument("--refresh", metavar="TARGET", help="print full watched text for rewriting notes")
    ap.add_argument("--commit", action="store_true", help="with --refresh: store fingerprints")
    ap.add_argument("--suggest", action="store_true", help="data-backed model and effort for a task type")
    ap.add_argument("--type", help="with --suggest: the task type (types/<type>.md)")
    ap.add_argument("--session-model", help="with --suggest: the model this conversation runs on")
    ap.add_argument("--run-length", choices=("short", "long"))
    ap.add_argument("--language")
    ap.add_argument("--style", help="image style")
    ap.add_argument("--input", choices=("text", "image"),
                    help="what the generator starts from: image means editing one (image) or a start frame (video)")
    ap.add_argument("--surface", choices=("api", "plan", "tool"), default="api")
    a = ap.parse_args(argv)
    a.offline = offline_reason(a.offline) is not None
    ctx = make_ctx(a.offline)

    if a.suggest:
        if not a.type:
            ap.error("--suggest needs --type")
        return suggest(a, ctx)

    if a.lineup:
        print((OFFLINE_LINE + "\n" if a.offline else "") + report.lineup_report(ctx))
        return 0
    if a.check_all:
        text, n = report.check_all(ctx)
        print((OFFLINE_LINE + "\n" if a.offline else "") + text)
        return 1 if n else 0
    if a.commit and not a.refresh:
        ap.error("--commit needs --refresh")
    name = a.refresh or a.target
    if not name:
        ap.error("one of --target, --refresh, --lineup, --check-all is required")
    try:
        key, model = R.resolve(name, ctx.reg, R.note_ids_by_key(ctx.notes_dir, ctx.reg))
    except KeyError:
        print(f"promptgremlin: unknown target '{name}'. Known: {', '.join(sorted(ctx.reg))}",
              file=sys.stderr)
        return 2
    if a.refresh:
        if a.commit and not (ctx.notes_dir / f"{key}.md").exists():
            print(f"promptgremlin: no notes for '{key}'", file=sys.stderr)
            return 2
        print((OFFLINE_LINE + "\n" if a.offline else "") + report.refresh(key, ctx, commit=a.commit))
        return 0
    if not (ctx.notes_dir / f"{key}.md").exists():
        print(f"promptgremlin: no notes for '{key}'", file=sys.stderr)
        return 2
    text, _ = report.target_report(key, a.model or model, ctx)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
