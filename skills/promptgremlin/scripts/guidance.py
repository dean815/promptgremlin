#!/usr/bin/env python3
"""Current prompting guidance for one target, with freshness flags.

    guidance.py --target <name> [--model <id>] [--offline]
    guidance.py --lineup [--offline]
    guidance.py --check-all [--offline]
    guidance.py --refresh <target> [--commit] [--offline]

<name> may be a target key, an alias (chatgpt, claude), or a model (opus 5.5).
Exit: 0 ok; 1 --check-all found flags; 2 unknown target or no notes.
"""
import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pglib import registry as R  # noqa: E402
from pglib import report  # noqa: E402

SKILL_DIR = Path(__file__).resolve().parent.parent


def make_ctx(offline):
    reg_path = SKILL_DIR / "sources.json"
    return report.Ctx(reg=R.load(reg_path), reg_path=reg_path, notes_dir=SKILL_DIR / "targets",
                      offline=offline, today=dt.date.today(), now=dt.datetime.now())


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target")
    ap.add_argument("--model")
    ap.add_argument("--offline", action="store_true", help="cache and notes only, no network")
    ap.add_argument("--lineup", action="store_true", help="print every family's current models")
    ap.add_argument("--check-all", action="store_true", help="freshness report for every target")
    ap.add_argument("--refresh", metavar="TARGET", help="print full watched text for rewriting notes")
    ap.add_argument("--commit", action="store_true", help="with --refresh: store fingerprints")
    a = ap.parse_args(argv)
    ctx = make_ctx(a.offline)

    if a.lineup:
        print(report.lineup_report(ctx))
        return 0
    if a.check_all:
        text, n = report.check_all(ctx)
        print(text)
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
        print(report.refresh(key, ctx, commit=a.commit))
        return 0
    if not (ctx.notes_dir / f"{key}.md").exists():
        print(f"promptgremlin: no notes for '{key}'", file=sys.stderr)
        return 2
    text, _ = report.target_report(key, a.model or model, ctx)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
