[547. 省份数量](https://leetcode-cn.com/problems/number-of-provinces/)

有 `n` 个城市，其中一些彼此相连，另一些没有相连。如果城市 `a` 与城市 `b` 直接相连，且城市 `b` 与城市 `c` 直接相连，那么城市 `a` 与城市 `c` 间接相连。

**省份** 是一组直接或间接相连的城市，组内不含其他没有相连的城市。

给你一个 `n x n` 的矩阵 `isConnected` ，其中 `isConnected[i][j] = 1` 表示第 `i` 个城市和第 `j`个城市直接相连，而 `isConnected[i][j] = 0` 表示二者不直接相连。

返回矩阵中 **省份** 的数量。

**示例 1：**

![img](https://assets.leetcode.com/uploads/2020/12/24/graph1.jpg)

```
输入：isConnected = [[1,1,0],[1,1,0],[0,0,1]]
输出：2
```

**示例 2：**

![img](https://assets.leetcode.com/uploads/2020/12/24/graph2.jpg)

```
输入：isConnected = [[1,0,0],[0,1,0],[0,0,1]]
输出：3
```

提示：

1 <= n <= 200
n == isConnected.length
n == isConnected[i].length
`isConnected[i][j]` 为 1 或 0
`isConnected[i][i]` == 1
`isConnected[i][j] == isConnected[j][i]`

---

由题意可知：

- 1 <= n <= 200 数据量可以放心的用常规的dfs bfs
- isConnected 本身就是邻接矩阵
- 相当于求几个连通分量，可用并查集

## 方法一：并查集

执行用时：16 ms, 在所有 C++ 提交中击败了92.48%的用户

内存消耗：13.4 MB, 在所有 C++ 提交中击败了41.19%的用户

时间复杂度：`O(n^2logn)`

空间复杂度：`O(n)`

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
    int findCircleNum(vector<vector<int>>& isConnected) {
        int rows = isConnected.size();
        int cols = isConnected[0].size();
        if (rows == 1) return 1;

        UnionFind uf(rows);

        // 只用遍历一半就行
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (r < c) {  // 右上
                    if (isConnected[r][c] == 1)
                        uf.unite(r, c);
                }
            }
        }
        return uf.setCount;
    }
};
```

执行用时：44 ms, 在所有 Python3 提交中击败了74.87%的用户

内存消耗：15.3 MB, 在所有 Python3 提交中击败了47.20%的用户

```python
class UnionFind:
    def __init__(self, n):
        self.count = n
        self.parent = [i for i in range(n)] # 初始化节点i的父节点为i
        self.rank = [0] * n

    def find(self, i):
        # 递归查找根节点，如果节点i的父节点为本身就找到了根，结束递归
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, x, y):
        # 合并两个节点
        rootx = self.find(x)
        rooty = self.find(y)
        if rootx != rooty:
            if self.rank[rootx] < self.rank[rooty]:
                rootx, rooty = rooty, rootx
            self.parent[rooty] = rootx
            if self.rank[rootx] == self.rank[rooty]:
                self.rank[rootx] += 1
            self.count -= 1
            
    def is_connected(self, x, y):
        # 判断两个节点是否连通
        return self.find(x) == self.find(y)

    def disconnected(self, x):
        # 断开节点与他父亲的连接
        self.parent[x] = x
        self.rank[x] = 0


class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        cities = len(isConnected)
        uf = UnionFind(cities)
        for i in range(cities):
            for j in range(i):  # 无向图，只用扫描一半就好了，全扫也不影响结果
                if isConnected[i][j] == 1:
                    uf.union(i, j)
        return uf.count
```

## 方法二：dfs

时间复杂度：`O(n^2)`，其中 n 是城市的数量。需要遍历矩阵 n 中的每个元素

空间复杂度：`O(n)`，其中 n 是城市的数量。需要使用数组 visited 记录每个城市是否被访问过，数组长度是 n，递归调用栈的深度不会超过 n。

执行用时：36 ms, 在所有 Python3 提交中击败了96.05%的用户

内存消耗：15.5 MB, 在所有 Python3 提交中击败了32.91%的用户

```python
class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        cities = len(isConnected)
        visited = set()
        
        def dfs(node):
            visited.add(node)
            for i in range(cities):
                if isConnected[node][i] == 1 and i not in visited:
                    dfs(i)
        
        ans = 0
        for city in range(cities):
            if city not in visited:
                dfs(city)
                ans += 1
        return ans
```

执行用时：20 ms, 在所有 Go 提交中击败了88.46%的用户

内存消耗：6.5 MB, 在所有 Go 提交中击败了62.06%的用户

```go
func findCircleNum(isConnected [][]int) int {
	visited := make([]bool, len(isConnected))
	var dfs func(int)
	dfs = func(node int) {
		visited[node] = true
		for i, v := range isConnected[node] {
			if v == 1 && !visited[i] {
				dfs(i)
			}
		}
	}

	ans := 0
	for city := 0; city < len(isConnected); city++ {
		if !visited[city] {
			dfs(city)
			ans++
		}
	}
	return ans
}
```



## 方法三：bfs

时间复杂度：`O(n^2)`

空间复杂度：`O(n)`

执行用时：36 ms, 在所有 Python3 提交中击败了96.05%的用户

内存消耗：15.2 MB, 在所有 Python3 提交中击败了82.20%的用户

```python
class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        cities = len(isConnected)
        visited = set()
        
        def bfs(node):
            queue = [node]
            visited.add(node)
            while queue:
                cur = queue.pop(0)
                for n_node in range(cities):
                    if isConnected[cur][n_node] == 1 and n_node not in visited:
                        queue.append(n_node)
                        visited.add(n_node)
                        
        ans = 0
        for city in range(cities):
            if city not in visited:
                bfs(city)
                ans += 1
        return ans
```

执行用时：20 ms, 在所有 Go 提交中击败了88.46%的用户

内存消耗：6.5 MB, 在所有 Go 提交中击败了96.50%的用户

```go
func findCircleNum(isConnected [][]int) int {
	visited := make([]bool, len(isConnected))
	var bfs func(int)
	bfs = func(node int) {
		queue := []int{node}
		visited[node] = true
		for len(queue) > 0 {
			cur := queue[0]
			queue = queue[1:]
			for i, v := range isConnected[cur] {
				if v == 1 && !visited[i] {
					queue = append(queue, i)
					visited[i] = true
				}
			}
		}
	}

	ans := 0
	for city := 0; city < len(isConnected); city++ {
		if !visited[city] {
			bfs(city)
			ans++
		}
	}
	return ans
}
```
