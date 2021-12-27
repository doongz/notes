#### [200. 岛屿数量](https://leetcode-cn.com/problems/number-of-islands/)

**方法一：bfs**

时间复杂度：`O(n^3)`

空间复杂度：`O(n^2)`

执行用时：112 ms, 在所有 Python3 提交中击败了59.56%的用户

内存消耗：23.5 MB, 在所有 Python3 提交中击败了87.32%的用户

```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        # 时间复杂度 O(n^3)
        rows = len(grid)
        cols = len(grid[0])

        def bfs(row, col):
            queue = [(row, col)]
            visited = set([(row, col)]) # 其实不用这个也不会走回头路
            while queue:
                r, c = queue.pop(0)
                grid[r][c] = "2"
                for dr, dc in ((0,1),(1,0),(-1,0),(0,-1)):
                    nr = r + dr
                    nc = c + dc
                    if 0<=nr<rows and 0<=nc<cols and grid[nr][nc] == "1" and (nr, nc) not in visited:
                        queue.append((nr, nc))
                        visited.add((nr, nc))

        cnt = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    bfs(r, c)
                    cnt += 1
        return cnt
```

**方法二：dfs**

执行用时：104 ms, 在所有 Python3 提交中击败了75.42%的用户

内存消耗：23.5 MB, 在所有 Python3 提交中击败了81.95%的用户

```go
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        # 时间复杂度 O(n^3)
        rows = len(grid)
        cols = len(grid[0])

        def dfs(row, col):
            grid[row][col] = "2"
            for dr, dc in ((0,1), (1,0), (0,-1), (-1,0)):
                nr = row + dr
                nc = col + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                    dfs(nr, nc)
 

        cnt = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "1":
                    dfs(r, c)
                    cnt += 1
        return cnt
```

