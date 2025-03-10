#ifndef DEBUG_H
#define DEBUG_H

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

    string centeredHeader(const string& text, int width = 60) {
        int pad = (width - (int)text.size()) / 2;
        if (pad < 0) pad = 0;
        return string(pad, '-') + " " + text + " " + string(pad, '-');
    }

    struct Debugger {
        Debugger() { debug_start = chrono::steady_clock::now(); }
        ~Debugger() {
            static istream* pIn;
            if (pIn == &cin) return;

            auto end = chrono::steady_clock::now();
            long long time_taken = chrono::duration_cast<chrono::milliseconds>(end - debug_start).count();

            ifstream actualFile("test.out");
            vector<string> actualLines;
            string line;
            while (getline(actualFile, line)) actualLines.push_back(line);

            ifstream expectedFile("test-expected.out");
            vector<string> expectedLines;
            while (getline(expectedFile, line)) expectedLines.push_back(line);

            cerr << "\n" << string(60, '=') << "\n";
            cerr << centeredHeader("DEBUG SUMMARY") << "\n";
            cerr << string(60, '=') << "\n\n";

            cerr << centeredHeader("OUTPUT") << "\n";
            for (auto &l : actualLines) cerr << "  " << l << "\n";
            if (actualLines.empty()) cerr << "  (no output)\n";
            cerr << "\n";

            cerr << centeredHeader("EXPECTED OUTPUT") << "\n";
            for (auto &l : expectedLines) cerr << "  " << l << "\n";
            if (expectedLines.empty()) cerr << "  (none provided)\n";
            cerr << "\n";

            cerr << centeredHeader("COMPARISON") << "\n";
            int total = (int)expectedLines.size(), passed = 0;
            for (int i = 0; i < total; i++) {
                if (i < (int)actualLines.size() && expectedLines[i] == actualLines[i]) passed++;
            }
            if (total == 0) cerr << "  No expected output provided.\n";
            else if (passed == total) cerr << " All test cases passed (" << passed << "/" << total << ")\n";
            else cerr << (total - passed) << " test case(s) failed (" << passed << "/" << total << ")\n";
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

#endif // DEBUG_H
