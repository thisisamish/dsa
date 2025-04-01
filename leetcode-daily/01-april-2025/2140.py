class Solution:
    def mostPoints(self, questions: List[List[int]]) -> int:
        n = len(questions)
        dp = [-1] * n
        dp[n - 1] = questions[n - 1][0]

        for i in range(n - 2, -1, -1):
            next_index = i + questions[i][1] + 1
            solve = questions[i][0] + (dp[next_index] if next_index < n else 0)
            dp[i] = max(solve, dp[i + 1])

        return dp[0]