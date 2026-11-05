#!/usr/bin/env python3
"""Run every test_* function in tests/test_*.py, and in <repo>/tools/tests and
<repo>/evals/guided/tests when this runs from the dev repo (the snapshot builder's and the bench's).
An installed plugin has neither, and they are skipped. Stdlib only. Exit 1 on any failure.

    run_tests.py [filter]   filter matches "<module>.<test name>" as a substring
"""
import importlib
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "tests"))
# <repo>/plugin/skills/promptgremlin/scripts: the repo is three levels above the skill folder.
# Only a checkout with the marketplace file at its root counts, so an installed copy skips these.
REPO = HERE.parents[3] if len(HERE.parents) > 3 else HERE
IN_REPO = (REPO / ".claude-plugin" / "marketplace.json").is_file() and (REPO / "plugin").resolve() == HERE.parents[2]
TOOLS = REPO / "tools"
DIRS = [HERE / "tests"]
if IN_REPO and (TOOLS / "tests").is_dir():
    sys.path[:0] = [str(TOOLS), str(TOOLS / "tests")]
    DIRS.append(TOOLS / "tests")
EVALS = REPO / "evals" / "guided" / "tests"
if IN_REPO and EVALS.is_dir():
    sys.path.insert(0, str(EVALS))
    DIRS.append(EVALS)


def main(pattern=""):
    fails = 0
    for path in [p for d in DIRS for p in sorted(d.glob("test_*.py"))]:
        mod = importlib.import_module(path.stem)
        for name, fn in list(vars(mod).items()):
            if name.startswith("test_") and callable(fn) and pattern in f"{path.stem}.{name}":
                try:
                    fn()
                    print(f"ok   {path.stem}.{name}")
                except Exception:
                    fails += 1
                    print(f"FAIL {path.stem}.{name}")
                    traceback.print_exc()
    print(f"\n{'FAILED' if fails else 'passed'}: {fails} failure(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
