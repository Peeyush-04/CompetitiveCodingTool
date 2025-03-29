/*
ID: ${USERNAME}
TASK: ${TASK}
LANG: ${LANGUAGE}
 */

import java.io.*;
import java.nio.file.*;
import java.util.*;

public class Main {
    static long startTime;

    public static void main(String[] args) throws Exception {
        startTime = System.currentTimeMillis();

        // Redirect input/output if test.in exists
        if (Files.exists(Paths.get("test.in"))) {
            System.setIn(new FileInputStream("test.in"));
            System.setOut(new PrintStream(new FileOutputStream("test.out")));
        }

        Scanner sc = new Scanner(System.in);
        int T = sc.hasNextInt() ? sc.nextInt() : 1;
        for (int i = 0; i < T; i++) {
            solve(sc);
        }
        if (System.getenv("LOCAL_DEBUG") != null) {
            debugSummary();
        }
        sc.close();
    }

    /**
     * A separate function that contains the “solution” logic for each test case.
     */
    static void solve(Scanner sc) {
        // code here
        
    }

    static String centeredHeader(String text, int width) {
        int pad = (width - text.length()) / 2;
        if (pad < 0) pad = 0;
        String dashes = new String(new char[pad]).replace("\0", "-");
        return dashes + " " + text + " " + dashes;
    }

    /**
     * Debug summary logic that writes to debug.out.
     */
    static void debugSummary() throws Exception {
        List<String> actualLines = new ArrayList<>();
        List<String> expectedLines = new ArrayList<>();

        if (Files.exists(Paths.get("test.out"))) {
            for (String line : Files.readAllLines(Paths.get("test.out"))) {
                line = line.trim();
                if (!line.isEmpty()) {
                    actualLines.add(line);
                }
            }
        }

        if (Files.exists(Paths.get("test-expected.out"))) {
            for (String line : Files.readAllLines(Paths.get("test-expected.out"))) {
                line = line.trim();
                if (!line.isEmpty()) {
                    expectedLines.add(line);
                }
            }
        }

        try (PrintWriter debug = new PrintWriter(new FileWriter("debug.out", false))) {
            debug.println(new String(new char[60]).replace("\0", "="));
            debug.println(centeredHeader("DEBUG SUMMARY", 60));
            debug.println(new String(new char[60]).replace("\0", "="));
            debug.println();

            debug.println(centeredHeader("OUTPUT", 60));
            for (String l : actualLines) {
                debug.println("  " + l);
            }
            if (actualLines.isEmpty()) {
                debug.println("  (no output)");
            }
            debug.println();

            debug.println(centeredHeader("EXPECTED OUTPUT", 60));
            for (String l : expectedLines) {
                debug.println("  " + l);
            }
            if (expectedLines.isEmpty()) {
                debug.println("  (none provided)");
            }
            debug.println();

            debug.println(centeredHeader("COMPARISON", 60));
            int total = expectedLines.size();
            int passed = 0;
            for (int i = 0; i < total; i++) {
                if (i < actualLines.size() && actualLines.get(i).equals(expectedLines.get(i))) {
                    passed++;
                }
            }
            if (total == 0)
                debug.println("  No expected output provided.");
            else if (passed == total)
                debug.println(" All test cases passed (" + passed + "/" + total + ")");
            else
                debug.println(" " + (total - passed) + " test case(s) failed (" + passed + "/" + total + ")");
            debug.println();

            debug.println(centeredHeader("PERFORMANCE", 60));
            long timeTaken = System.currentTimeMillis() - startTime;
            debug.println("  Time taken:  " + timeTaken + " ms");
            debug.println(new String(new char[60]).replace("\0", "="));
        }
    }
}
