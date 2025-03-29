"""
ID: ${USERNAME}
TASK: ${TASK}
LANG: ${LANGUAGE}
"""

import sys, os, time, math, random, collections, itertools

def centeredHeader(text, width=60):
    pad = (width - len(text)) // 2
    if pad < 0:
        pad = 0
    return "-" * pad + " " + text + " " + "-" * pad

def debug_summary(start_time):
    end_time = time.time()
    time_taken = int((end_time - start_time) * 1000)
    
    actual_lines = []
    expected_lines = []
    
    if os.path.exists("test.out"):
        with open("test.out", "r") as f:
            actual_lines = [line.strip() for line in f if line.strip()]
    
    if os.path.exists("test-expected.out"):
        with open("test-expected.out", "r") as f:
            expected_lines = [line.strip() for line in f if line.strip()]
    
    # Print debug summary directly to the console
    print("\n" + "=" * 60)
    print(centeredHeader("DEBUG SUMMARY"))
    print("=" * 60 + "\n")
    
    print(centeredHeader("OUTPUT"))
    for l in actual_lines:
        print("  " + l)
    if not actual_lines:
        print("  (no output)")
    print()
    
    print(centeredHeader("EXPECTED OUTPUT"))
    for l in expected_lines:
        print("  " + l)
    if not expected_lines:
        print("  (none provided)")
    print()
    
    print(centeredHeader("COMPARISON"))
    total = len(expected_lines)
    passed = sum(1 for i in range(total) if i < len(actual_lines) and actual_lines[i] == expected_lines[i])
    if total == 0:
        print("  No expected output provided.")
    elif passed == total:
        print(" All test cases passed ({}/{})".format(passed, total))
    else:
        print(" {} test case(s) failed ({}/{})".format(total - passed, passed, total))
    print()
    
    print(centeredHeader("PERFORMANCE"))
    print("  Time taken:  {} ms".format(time_taken))
    # Memory usage is not directly available; can be added if needed with additional libraries
    print("=" * 60)

def solve():
    # code here
    
    pass

def main():
    start_time = time.time()
    
    # Redirect I/O if test.in exists
    if os.path.exists("test.in"):
        sys.stdin = open("test.in", "r")
        sys.stdout = open("test.out", "w")
    
    # -------------------- Start Solution Section --------------------
    try:
        T = int(input())
    except:
        T = 1
    for _ in range(T):
        solve()
        pass
    # -------------------- End Solution Section --------------------
    
    if os.environ.get("LOCAL_DEBUG"):
        debug_summary(start_time)

if __name__ == "__main__":
    main()
