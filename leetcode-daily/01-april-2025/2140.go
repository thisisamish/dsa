func mostPoints(questions [][]int) int64 {
    n := len(questions)
    dp := make([]int64, n)
    for i := range dp {
        dp[i] = -1
    }
    dp[n - 1] = int64(questions[n - 1][0])

    for i := n - 2; i >= 0; i-- {
        nextIndex := i + questions[i][1] + 1
        solve := int64(questions[i][0]) 
        if nextIndex < n {
            solve += dp[nextIndex]
        }
        dp[i] = max(solve, dp[i + 1])
    }

    return dp[0]
}