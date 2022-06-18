题目：[329. 矩阵中的最长递增路径](https://leetcode.cn/problems/longest-increasing-path-in-a-matrix/)

## 方法一：记忆化 dfs

dfs 返回从 [r,c] 出发的最长递增路径长度

时间复杂度：`O(mn)`

空间复杂度：`O(mn)`

```c++
class Solution {
public:
    int rows;
    int cols;
    vector<vector<int>> matrix;
    vector<vector<int>> memo;
    vector<pair<int, int>> directions = {{1, 0}, {0, 1}, {-1, 0}, {0, -1}};

    // 返回从 [r,c] 出发的最长递增路径长度
    int dfs(int r, int c) {
        if (memo[r][c] != -1) return memo[r][c];

        int res = 1;
        for (auto& [dr, dc] : directions) {
            int nr = r + dr;
            int nc = c + dc;
            if (0 <= nr && nr < rows && 0 <= nc && nc < cols) {
                if (matrix[nr][nc] > matrix[r][c]) {
                    res = max(res, dfs(nr, nc) + 1);
                }
            }
        }
        memo[r][c] = res;
        return memo[r][c];
    }

    int longestIncreasingPath(vector<vector<int>>& matrix) {
        rows = matrix.size();
        cols = matrix[0].size();
        memo.resize(rows, vector<int>(cols, -1));
        this->matrix = matrix;

        int ans = INT_MIN;
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                ans = max(ans, dfs(r, c));
            }
        }
        return ans;
    }
};
```



```python
class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:

        rows = len(matrix)
        cols = len(matrix[0])
        memo = [[-1 for _ in range(cols)] for _ in range(rows)]
        # 记录从[r][c]开始走的最长距离
        # 如果下次又走到了[r][c]，直接用它的结果

        def dfs(row, col):
            if memo[row][col] != -1:
                return memo[row][col]
            memo[row][col] = 1
            for dr, dc in ((0, 1), (1, 0), (-1, 0), (0, -1)):
                nr = row + dr
                nc = col + dc
                if 0<=nr<rows and 0<=nc<cols and matrix[nr][nc] > matrix[row][col]:
                    memo[row][col] = max(memo[row][col], dfs(nr, nc)+1)
            return memo[row][col]

        ans = float("-inf")  
        for r in range(rows):
            for c in range(cols):
                ans = max(ans, dfs(r, c))
        return ans
```

## 方法二：拓扑排序





**bfs memo记录 走到[r] [c]用了几步**

**dfs memo记录 从[r] [c]开始走到终点的最长距离**

记忆化bfs: 1720 ms 15.6 MB

```python
class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:

        rows = len(matrix)
        cols = len(matrix[0])
        memo = [[-1 for _ in range(cols)] for _ in range(rows)]
        # 记录上次走到[r][c]的时候用了几步，如果这次又走到[r][c]，
        # 这次走到[r][c]的步数比上次还要少，那就没必要再走了，
        # 如果这次走的步数多，就更新

        def bfs(row, col):
            queue = collections.deque()
            queue.append((row, col, 1))
            while queue:
                r, c, step = queue.popleft()
                for dr, dc in ((0, 1), (1, 0), (-1, 0), (0, -1)):
                    nr = r + dr
                    nc = c + dc
                    if 0<=nr<rows and 0<=nc<cols and matrix[nr][nc]>matrix[r][c]:
                        if step+1 <= memo[nr][nc]:
                            continue
                        queue.append((nr, nc, step+1))
                        memo[nr][nc] = step + 1
            return step

        ans = float("-inf")
        for r in range(rows):
            for c in range(cols):
                ans = max(ans, bfs(r, c))
        return ans
```



拓扑排序：288 ms 19.6 MB

时间复杂度：O(mn) 空间复杂度：O(mn)

```python
class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:

        rows = len(matrix)
        cols = len(matrix[0])
        adj_list = collections.defaultdict(list) # 邻接表
        in_degrees = [[0 for _ in range(cols)] for _ in range(rows)] # 入度

        for r in range(rows):
            for c in range(cols):
                for dr, dc in ((0,1),(1,0),(0,-1),(-1,0)):
                    nr = r + dr
                    nc = c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if matrix[nr][nc] < matrix[r][c]:
                            # 因为要入度，所以要小于
                            in_degrees[r][c] += 1
                        elif matrix[nr][nc] > matrix[r][c]:
                            # 方向为从小指向大，所以要大于
                            adj_list[(r, c)].append((nr, nc))
        # print(adj_list)
        # print(in_degrees)

        # 从入度为0开始找，才能找到最长的
        queue = collections.deque()
        for r in range(rows):
            for c in range(cols):
                if in_degrees[r][c] == 0:
                    queue.append((r, c))
        # print(queue)

        step = 0
        while queue:
            # 这个跟课程表I那个题不一样，需要一层一层的出列，而不是一个一个的出
            sz = len(queue)
            for _ in range(sz):
                r, c = queue.popleft()
                for nr, nc in adj_list[(r, c)]:
                    in_degrees[nr][nc] -= 1
                    if in_degrees[nr][nc] == 0:
                        # 入度为0的才能入队列，因为不为0的可能会被其他的走出最长距离
                        # 难点在于课程表那题明确告知了依赖关系，这道题需要想明白为什么沿着入度为0的走
                        queue.append((nr, nc))
            step += 1
        return step
```

