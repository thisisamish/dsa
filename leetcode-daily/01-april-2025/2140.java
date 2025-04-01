class Solution {
    public long mostPoints(int[][] questions) {
        int n = questions.length;
        long[] dp = new long[n];
        dp[n - 1] = questions[n - 1][0];

        for (int i = n - 2; i >= 0; i--) {
            int nextIndex = i + questions[i][1] + 1;
            long solve = questions[i][0] + (nextIndex < n ? dp[nextIndex] : 0);
            dp[i] = Math.max(solve, dp[i + 1]);
        }

        return dp[0];
    }
}