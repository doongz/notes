bfs: 240 ms 16.2 MB

```python
class Solution:
    def numSquares(self, n: int) -> int:
        queue = collections.deque()
        queue.append((n, 0))
        visited = set()

        while queue:
            cur, step = queue.popleft()
            next_list = [cur-i*i for i in range(1, int(cur**0.5)+1)]
            for n_node in next_list:
                if n_node == 0:
                    return step+1
                if n_node not in visited:
                    queue.append((n_node, step+1))
                    visited.add(n_node)
        return -1
```

dp: 3888 ms 15.1 MB

```python
class Solution:
    def numSquares(self, n: int) -> int:

        nums = [i*i for i in range(1, int(n**0.5)+1)]
        dp = [0] + [float("inf") for _ in range(n)]

        for j in range(1, n+1):
            for num in nums:
                if j - num < 0:
                    continue
                dp[j] = min(dp[j], dp[j-num]+1)
        return dp[-1]
```

dp: 2860 ms 15.2 MB

```python
class Solution:
    def numSquares(self, n: int) -> int:

        nums = [i*i for i in range(1, int(n**0.5)+1)]
        dp = [0] + [float('inf')]*n
        for num in nums: # 减少了 j - num < 0 的判断
            for j in range(num, n+1):
                dp[j] = min(dp[j], dp[j-num]+1)
        return dp[-1]
```

贪心：48 ms 15.4 MB

```python
class Solution:
    def numSquares(self, n: int) -> int:

        nums = set(i*i for i in range(1, int(n**0.5)+1))

        def dfs(num, count):
            if count == 1: # 当只有1次的时候，无论如何都要返回一下结果
                return num in nums
            for p in nums:
                if dfs(num-p, count-1):
                    return True
            return False
        
        for count in range(1, n+1): # 可能找到的次数，1次就找到，2次...
            if dfs(n, count):
                return count
```