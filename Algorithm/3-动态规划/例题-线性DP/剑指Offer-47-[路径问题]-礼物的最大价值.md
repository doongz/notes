题目：[剑指 Offer 47. 礼物的最大价值](https://leetcode.cn/problems/li-wu-de-zui-da-jie-zhi-lcof/)

```python
class Solution:
    def maxValue(self, grid: List[List[int]]) -> int:
        # 路径dp，dp[r][c] 表示到达 r,c 的最大礼物价值
        rows = len(grid)
        cols = len(grid[0])
        dp = [[0 for _ in range(cols)] for _ in range(rows)]

        # 初始化上边和左边
        dp[0][0] = grid[0][0]
        for r in range(1, rows):
            dp[r][0] = dp[r-1][0] + grid[r][0]
        for c in range(1, cols):
            dp[0][c] = dp[0][c-1] + grid[0][c]

        # 当前位置，可能从上边和左边转移过来，去最大值
        for r in range(1, rows):
            for c in range(1, cols):
                dp[r][c] = max(dp[r][c-1], dp[r-1][c]) + grid[r][c]
        
        return dp[rows-1][cols-1]
```

