[200. 岛屿数量](https://leetcode-cn.com/problems/number-of-islands/)

## 方法一：并查集

执行用时：32 ms, 在所有 C++ 提交中击败了63.65%的用户

内存消耗：13.3 MB, 在所有 C++ 提交中击败了26.30%的用户

```c++
class UnionFind {
public:
    vector<int> parent;  // 下标idx为节点，parent[idx]为该节点的父亲
    vector<int> size;    // 若idx为父亲根节点，size[idx]为该连通分量的大小
    int n;               // 节点数量
    int setCount;        // 连通分量的数量

public:
    UnionFind(int _n) : n(_n), setCount(_n), parent(_n), size(_n, 1) {
        iota(parent.begin(), parent.end(), 0);
    }

    int find(int x) {
        return parent[x] == x ? x : parent[x] = find(parent[x]);
    }

    bool unite(int x, int y) {
        x = find(x);
        y = find(y);
        if (x == y) return false;

        if (size[x] < size[y]) {
            swap(x, y);
        }
        parent[y] = x;       // x 作为 y 的父亲
        size[x] += size[y];  // 父亲节点x的联通分量大小加上y节点的
        --setCount;
        return true;
    }

    bool is_connected(int x, int y) {
        x = find(x);
        y = find(y);
        return x == y;
    }

    void disconnected(int x) {
        if (x != parent[x]) {
            parent[x] = x;
            size[x] = 1;
            ++setCount;
        }
    }
};

class Solution {
public:
    int numIslands(vector<vector<char>>& grid) {
        int rows = grid.size();
        int cols = grid[0].size();

        UnionFind uf(rows * cols);
        vector<pair<int, int>> direction = {{0, 1}, {1, 0}, {-1, 0}, {0, -1}};
        auto node = [&](int r, int c) {
            return r * cols + c;
        };
        int zeorCnt = 0;  // 因为0没联通，所以并查集中每个0各自为一个联通分量
        // 如果当前节点为1，就把它和周边的1联通
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == '0') {
                    zeorCnt++;
                    continue;
                }
                for (auto d : direction) {
                    int nr = r + d.first;
                    int nc = c + d.second;
                    if (0 <= nr && nr < rows && 0 <= nc && nc < cols && grid[nr][nc] == '1') {
                        uf.unite(node(r, c), node(nr, nc));
                    }
                }
            }
        }
        // for (int i = 0;i<uf.parent.size();i++) {
        //     cout << uf.parent[i] << " ";
        // }
        // cout << endl;
        // cout <<uf.setCount << " " <<zeorCnt << endl;
        // 1的联通分量 = 总的连通分量 - 0的联通分量
        return uf.setCount - zeorCnt;
    }
};
```

## 方法二：bfs

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

## 方法三：dfs

执行用时：104 ms, 在所有 Python3 提交中击败了75.42%的用户

内存消耗：23.5 MB, 在所有 Python3 提交中击败了81.95%的用户

```python
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