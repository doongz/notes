题目：[LCP 07. 传递信息](https://leetcode-cn.com/problems/chuan-di-xin-xi/)

## 方法一：dfs

```c++
class Solution {
public:
    int end;
    unordered_map<int, vector<int>> adj;  // 临接表

    // 从 cur 位置，再走 k 步，能到达 n-1 位置的方案数
    int dfs(int cur, int k) {
        // 走的终点，且剩余步数为0
        if (k == 0) {
            if (cur == end) {
                return 1;
            } else {
                return 0;
            }
        }
        int cnt = 0;
        for (int next : adj[cur]) {
            cnt += dfs(next, k - 1);
        }
        return cnt;
    }
    int numWays(int n, vector<vector<int>>& relation, int k) {
        end = n - 1;
        for (vector<int> r : relation) {
            adj[r[0]].push_back(r[1]);
        }
        return dfs(0, k);
    }
};
```

## 方法二：记忆化搜索

「子问题」为站在 cur 位置上，还有 k 步

对此使用记忆化

时间复杂度：`O(n * k)`

空间复杂度：`O(n * k)`

```c++
class Solution {
public:
    int end;
    unordered_map<int, vector<int>> adj;  // 临接表

    // 从 cur 位置，再走 k 步，能到达 n-1 位置的方案数
    int dfs(int cur, int k, vector<vector<int>>& memo) {
        // 走的终点，且剩余步数为0
        if (k == 0) {
            if (cur == end) {
                return 1;
            } else {
                return 0;
            }
        }
        if (memo[cur][k] != -1) return memo[cur][k];

        int cnt = 0;
        for (int next : adj[cur]) {
            cnt += dfs(next, k - 1, memo);
        }
        memo[cur][k] = cnt;
        return cnt;
    }

    int numWays(int n, vector<vector<int>>& relation, int k) {
        end = n - 1;
        for (vector<int> r : relation) {
            adj[r[0]].push_back(r[1]);
        }
        vector<vector<int>> memo(n, vector<int>(k + 1, -1));
        return dfs(0, k, memo);
    }
};
```

