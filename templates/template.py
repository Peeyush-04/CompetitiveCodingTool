"""
ID: ${USERNAME}
TASK: ${TASK}
LANG: ${LANGUAGE}
"""

import sys
import time
import atexit

_debug_start = time.time()

def debug_summary():
    try:
        with open("test.out", "r") as f:
            actual = [line.strip() for line in f if line.strip()]
    except Exception:
        actual = []
    try:
        with open("test-expected.out", "r") as f:
            expected = [line.strip() for line in f if line.strip()]
    except Exception:
        expected = []
    print("=" * 60, file=sys.stderr)
    print("DEBUG SUMMARY", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    print("OUTPUT:", file=sys.stderr)
    if not actual:
        print("  (no output)", file=sys.stderr)
    else:
        for line in actual:
            print("  " + line, file=sys.stderr)
    print("\nEXPECTED OUTPUT:", file=sys.stderr)
    if not expected:
        print("  (none provided)", file=sys.stderr)
    else:
        for line in expected:
            print("  " + line, file=sys.stderr)
    print("\nCOMPARISON:", file=sys.stderr)
    total = len(expected)
    passed = sum(1 for a, e in zip(actual, expected) if a == e)
    if total == 0:
        print("  No expected output provided.", file=sys.stderr)
    elif passed == total:
        print("  All test cases passed ({}/{})".format(passed, total), file=sys.stderr)
    else:
        print("  {} test case(s) failed ({}/{})".format(total - passed, passed, total), file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    elapsed = int((time.time() - _debug_start) * 1000)
    print("PERFORMANCE:", file=sys.stderr)
    print("  Time taken: {} ms".format(elapsed), file=sys.stderr)

atexit.register(debug_summary)

def solve():
    # code here
    
    pass

if __name__ == "__main__":
    data = sys.stdin.read().splitlines()
    T = int(data[0])
    for _ in range(T):
        solve()
