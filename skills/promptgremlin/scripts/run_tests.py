#!/usr/bin/env python3
"""Run every test_* function in tests/test_*.py. Stdlib only. Exit 1 on any failure.

    run_tests.py [filter]   filter matches "<module>.<test name>" as a substring
"""
import importlib
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "tests"))


def main(pattern=""):
    fails = 0
    for path in sorted((HERE / "tests").glob("test_*.py")):
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
