/*
ID: ${USERNAME}
TASK: ${TASK}
LANG: ${LANGUAGE}
*/
import java.io.*;
import java.util.*;

public class Main {
    private static long debugStart = System.currentTimeMillis();

    static {
        // Register a shutdown hook to output debug information.
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            try {
                List<String> actual = readLines("test.out");
                List<String> expected = readLines("test-expected.out");
                System.err.println("============================================================");
                System.err.println("DEBUG SUMMARY");
                System.err.println("============================================================");
                System.err.println("OUTPUT:");
                if (actual.isEmpty()) {
                    System.err.println("  (no output)");
                } else {
                    for (String line : actual) {
                        System.err.println("  " + line);
                    }
                }
                System.err.println("\nEXPECTED OUTPUT:");
                if (expected.isEmpty()) {
                    System.err.println("  (none provided)");
                } else {
                    for (String line : expected) {
                        System.err.println("  " + line);
                    }
                }
                System.err.println("\nCOMPARISON:");
                int total = expected.size();
                int passed = 0;
                for (int i = 0; i < Math.min(actual.size(), expected.size()); i++) {
                    if (actual.get(i).equals(expected.get(i))) {
                        passed++;
                    }
                }
                if (total == 0) {
                    System.err.println("  No expected output provided.");
                } else if (passed == total) {
                    System.err.println("  All test cases passed (" + passed + "/" + total + ")");
                } else {
                    System.err.println("  " + (total - passed) + " test case(s) failed (" + passed + "/" + total + ")");
                }
                System.err.println("============================================================");
                long elapsed = System.currentTimeMillis() - debugStart;
                System.err.println("PERFORMANCE:");
                System.err.println("  Time taken: " + elapsed + " ms");
            } catch (Exception e) {
                e.printStackTrace();
            }
        }));
    }

    private static List<String> readLines(String filename) {
        List<String> lines = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = br.readLine()) != null) {
                line = line.trim();
                if (!line.isEmpty()) {
                    lines.add(line);
                }
            }
        } catch (Exception e) {
            // If file not found or error, return empty list.
            // Optionally, print an error message:
            System.err.println("Error reading file: " + filename + " - " + e.getMessage());
        }
        return lines;
    }

    public static void solve() {
        // code here
        
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int T = Integer.parseInt(br.readLine());
        while (T-- > 0) {
            solve();
        }
    }
}
