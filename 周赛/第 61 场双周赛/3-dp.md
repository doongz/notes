```python
import collections

class Solution:
    def run(self, n, rides):
        store = collections.defaultdict(list)
        for s, e, t in rides:
            store[e].append((s, e-s+t))
        dp = [0] * n  # dp[i]表示到i点时最大的收益
        for i in range(n):
            dp[i] = max(dp[i-1], dp[i]) # 初始化dp[i]
            for s, e in store[i+1]: # dp里面的index要比store少1
                dp[i] = max(dp[i], dp[s-1]+e)
        return dp[-1]


if __name__ == "__main__":
    n = 20
    rides = [[1, 6, 1], [3, 10, 2], [10, 12, 3],
             [11, 12, 2], [12, 15, 2], [13, 18, 1]]
    res = Solution().run(n, rides)
    print(res)
```