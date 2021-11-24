dp: 1216 ms 15.3 MB

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:

        dp = [0] + [float("inf") for _ in range(amount)]

        for i in range(1, amount+1):
            for c in coins:
                if i - c < 0:
                    continue
                dp[i] = min(dp[i], dp[i-c]+1)
                
        if dp[-1] == float("inf"):
            return -1
        else:
            return dp[-1]
```

dp优化: 1068 ms 15.3 MB

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:

        dp = [0] + [float("inf") for _ in range(amount)]

        for c in coins:
            for i in range(c, amount+1):
                dp[i] = min(dp[i], dp[i-c]+1)

        if dp[-1] == float("inf"):
            return -1
        else:
            return dp[-1]
```

bfs: 636 ms 16 MB

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:

        if amount == 0:
            return 0

        queue = collections.deque()
        queue.append((amount, 0))
        visited = set()
        
        while queue:
            cur, step = queue.popleft()
            for coin in coins:
                if cur - coin < 0:
                    continue
                elif cur - coin == 0:
                    return step + 1
                next_node = cur-coin
                if next_node in visited:
                    continue
                queue.append((next_node, step+1))
                visited.add(next_node)
        return -1
```



