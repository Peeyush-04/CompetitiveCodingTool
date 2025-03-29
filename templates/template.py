"""
ID: ${USERNAME}
TASK: ${TASK}
LANG: ${LANGUAGE}
"""

import sys
import time
import os

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
        with open("test.out") as f:
            actual_lines = [line.strip() for line in f if line.strip()]
    if os.path.exists("test-expected.out"):
        with open("test-expected.out") as f:
            expected_lines = [line.strip() for line in f if line.strip()]

    with open("debug.out", "a") as debug:
        debug.write("\n" + "=" * 60 + "\n")
        debug.write(centeredHeader("DEBUG SUMMARY") + "\n")
        debug.write("=" * 60 + "\n\n")
        
        debug.write(centeredHeader("OUTPUT") + "\n")
        for l in actual_lines:
            debug.write("  " + l + "\n")
        if not actual_lines:
            debug.write("  (no output)\n")
        debug.write("\n")
        
        debug.write(centeredHeader("EXPECTED OUTPUT") + "\n")
        for l in expected_lines:
            debug.write("  " + l + "\n")
        if not expected_lines:
            debug.write("  (none provided)\n")
        debug.write("\n")
        
        debug.write(centeredHeader("COMPARISON") + "\n")
        total = len(expected_lines)
        passed = sum(1 for i in range(total) if i < len(actual_lines) and actual_lines[i] == expected_lines[i])
        if total == 0:
            debug.write("  No expected output provided.\n")
        elif passed == total:
            debug.write(" All test cases passed ({}/{})\n".format(passed, total))
        else:
            debug.write(" {} test case(s) failed ({}/{})\n".format(total - passed, passed, total))
        debug.write("\n")
        
        debug.write(centeredHeader("PERFORMANCE") + "\n")
        debug.write("  Time taken:  {} ms\n".format(time_taken))
        debug.write("=" * 60 + "\n")
        
def solve():
    #code here
    
    pass

def main():
    start_time = time.time()
    
    # Redirect input and output if test.in exists
    if os.path.exists("test.in"):
        sys.stdin = open("test.in")
        sys.stdout = open("test.out", "w")
    
    try:
        T = int(input())
    except:
        T = 1
    for _ in range(T):
        solve()

    if os.environ.get("LOCAL_DEBUG"):
        debug_summary(start_time)

if __name__ == '__main__':
    main()