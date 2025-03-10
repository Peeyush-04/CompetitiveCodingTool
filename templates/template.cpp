// Username: [USERNAME]
// Task: [TASK]
// Language: C++
// Created: [DATETIME]

#include "debug.h"
#include <iostream>
#include <fstream>
#include <algorithm>
#include <string>
#include <vector>
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
#include <cstdlib>
#include <cassert>
#include <stdexcept>
#include <sstream>

#ifdef __linux__
#include <sys/resource.h>
#endif

using namespace std;

#define int64 int64_t
#define int32 int32_t
#define ll long long

static istream* pIn = &cin;
static ostream* pOut = &cout;

#define cin  (*pIn)
#define cout (*pOut)

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

// --------------------
// Start Solution Section
// --------------------

int T = 1;

void solve() {
    // code here

}

int32 main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    setupIO();

    // cin >> T;
    while (T--) solve();

    return 0;
}
