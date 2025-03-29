/*
ID: ${USERNAME}
TASK: ${TASK}
LANG: ${LANGUAGE}
*/

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.lang.Math;

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
        // -------------------- Start Solution Section --------------------
        int T = sc.hasNextInt() ? sc.nextInt() : 1;
        for (int i = 0; i < T; i++) {
            solve(sc);
        }
        // -------------------- End Solution Section --------------------
        sc.close();
        
        if (System.getenv("LOCAL_DEBUG") != null) {
            debugSummary();
        }
    }
    
    static void solve(Scanner sc) {
        // code here
        
    }
    
    static String centeredHeader(String text, int width) {
        int pad = (width - text.length()) / 2;
        if (pad < 0) pad = 0;
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < pad; i++) sb.append("-");
        sb.append(" ").append(text).append(" ");
        for (int i = 0; i < pad; i++) sb.append("-");
        return sb.toString();
    }
    
    static void debugSummary() throws Exception {
        List<String> actualLines = new ArrayList<>();
        List<String> expectedLines = new ArrayList<>();
        
        if (Files.exists(Paths.get("test.out"))) {
            for (String line : Files.readAllLines(Paths.get("test.out"))) {
                line = line.trim();
                if (!line.isEmpty()) actualLines.add(line);
            }
        }
        
        if (Files.exists(Paths.get("test-expected.out"))) {
            for (String line : Files.readAllLines(Paths.get("test-expected.out"))) {
                line = line.trim();
                if (!line.isEmpty()) expectedLines.add(line);
            }
        }
        
        System.err.println();
        System.err.println("============================================================");
        System.err.println(centeredHeader("DEBUG SUMMARY", 60));
        System.err.println("============================================================\n");
        
        System.err.println(centeredHeader("OUTPUT", 60));
        for (String l : actualLines)
            System.err.println("  " + l);
        if (actualLines.isEmpty())
            System.err.println("  (no output)");
        System.err.println();
        
        System.err.println(centeredHeader("EXPECTED OUTPUT", 60));
        for (String l : expectedLines)
            System.err.println("  " + l);
        if (expectedLines.isEmpty())
            System.err.println("  (none provided)");
        System.err.println();
        
        System.err.println(centeredHeader("COMPARISON", 60));
        int total = expectedLines.size();
        int passed = 0;
        for (int i = 0; i < total; i++) {
            if (i < actualLines.size() && actualLines.get(i).equals(expectedLines.get(i)))
                passed++;
        }
        if (total == 0)
            System.err.println("  No expected output provided.");
        else if (passed == total)
            System.err.println(" All test cases passed (" + passed + "/" + total + ")");
        else
            System.err.println(" " + (total - passed) + " test case(s) failed (" + passed + "/" + total + ")");
        System.err.println();
        
        System.err.println(centeredHeader("PERFORMANCE", 60));
        long timeTaken = System.currentTimeMillis() - startTime;
        System.err.println("  Time taken:  " + timeTaken + " ms");
        System.err.println("============================================================");
    }
}
