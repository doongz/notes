题目：[剑指 Offer 47. 礼物的最大价值](https://leetcode.cn/problems/li-wu-de-zui-da-jie-zhi-lcof/)

在一个 m*n 的棋盘的每一格都放有一个礼物，每个礼物都有一定的价值（价值大于 0）。你可以从棋盘的左上角开始拿格子里的礼物，并每次向右或者向下移动一格、直到到达棋盘的右下角。给定一个棋盘及其上面的礼物的价值，请计算你最多能拿到多少价值的礼物？

**示例 1:**

```
输入: 
[
  [1,3,1],
  [1,5,1],
  [4,2,1]
]
输出: 12
解释: 路径 1→3→5→2→1 可以拿到最多价值的礼物
```

---

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

