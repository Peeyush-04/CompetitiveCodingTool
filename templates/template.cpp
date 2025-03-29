/*
ID: ${USERNAME}
TASK: ${TASK}
LANG: ${LANGUAGE}
*/

#ifdef LOCAL_DEBUG
#include <windows.h>
#include <psapi.h>
#include <chrono>
#include <fstream>
#include <iostream>
#include <vector>
#include <iomanip>
#include <sstream>
using namespace std;
static chrono::steady_clock::time_point debug_start;

// Helper function to trim whitespace
string trim(const string &s) {
    size_t start = s.find_first_not_of(" \t\n\r");
    size_t end = s.find_last_not_of(" \t\n\r");
    return (start == string::npos) ? "" : s.substr(start, end - start + 1);
}

string centeredHeader(const string& text, int width = 60) {
    int pad = (width - (int)text.size()) / 2;
    if (pad < 0) pad = 0;
    return string(pad, '-') + " " + text + " " + string(pad, '-');
}

struct Debugger {
    Debugger() { 
        debug_start = chrono::steady_clock::now(); 
    }
    ~Debugger() {
        auto end = chrono::steady_clock::now();
        long long time_taken = chrono::duration_cast<chrono::milliseconds>(end - debug_start).count();

        ifstream actualFile("test.out");
        vector<string> actualLines;
        string line;
        while (getline(actualFile, line)) {
            string t = trim(line);
            if (!t.empty()) actualLines.push_back(t);
        }

        ifstream expectedFile("test-expected.out");
        vector<string> expectedLines;
        while (getline(expectedFile, line)) {
            string t = trim(line);
            if (!t.empty()) expectedLines.push_back(t);
        }

        // Print debug summary directly to the command window (stderr)
        cerr << "\n" << string(60, '=') << "\n";
        cerr << centeredHeader("DEBUG SUMMARY") << "\n";
        cerr << string(60, '=') << "\n\n";

        cerr << centeredHeader("OUTPUT") << "\n";
        for (auto &l : actualLines) 
            cerr << "  " << l << "\n";
        if (actualLines.empty()) 
            cerr << "  (no output)\n";
        cerr << "\n";

        cerr << centeredHeader("EXPECTED OUTPUT") << "\n";
        for (auto &l : expectedLines) 
            cerr << "  " << l << "\n";
        if (expectedLines.empty()) 
            cerr << "  (none provided)\n";
        cerr << "\n";

        cerr << centeredHeader("COMPARISON") << "\n";
        int total = (int)expectedLines.size(), passed = 0;
        for (int i = 0; i < total; i++) {
            if (i < (int)actualLines.size() && expectedLines[i] == actualLines[i])
                passed++;
        }
        if (total == 0)
            cerr << "  No expected output provided.\n";
        else if (passed == total)
            cerr << " All test cases passed (" << passed << "/" << total << ")\n";
        else 
            cerr << (total - passed) << " test case(s) failed (" << passed << "/" << total << ")\n";
        cerr << "\n";

        cerr << centeredHeader("PERFORMANCE") << "\n";
        cerr << "  Time taken:  " << time_taken << " ms\n";
        PROCESS_MEMORY_COUNTERS pmc;
        if (GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc)))
            cerr << "  Memory used: " << (pmc.WorkingSetSize / 1024) << " KB\n";
        else
            cerr << "  Memory used: N/A\n";
        cerr << string(60, '=') << "\n";
    }
};
static Debugger _debugger;
#endif

// --------------------
// Start Solution Section
// --------------------

#include <iostream>
#include <fstream>
#include <algorithm>
#include <string>
#include <vector>
#include <array>
#include <list>
#include <stack>
#include <queue>
#include <unordered_map>
#include <map>
#include <unordered_set>
#include <set>
#include <numeric>
#include <stdint.h>
#include <cmath>
#include <climits>
#include <utility>
#include <chrono>
#include <functional>
#include <random>
using namespace std;

static istream* pIn = &cin;
static ostream* pOut = &cout;

#define cin (*pIn)
#define cout (*pOut)
#define ll long long
#define int32 int32_t
#define int64 int64_t

void setupIO() {
    static ifstream fin("test.in");
    if (fin.is_open()) {
        static ofstream fout("test.out");
        if (fout.is_open()) {
            pIn = &fin;
            pOut = &fout;
        }
    }
}

int T = ${T};

void solve() {
    // your solution code here
    
}

int32 main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    setupIO();
    // cin >> T;
    while (T--) solve();
    return 0;
}
