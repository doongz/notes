[514. 自由之路](https://leetcode-cn.com/problems/freedom-trail/)

## 方法一：记忆化搜索

思考：

- 是否具备最优子结构：
  - 向左转或向右转，构成了两个独立的结构
  - 当 key 为 deyde，若我们知道到达 d 的最优操作数 k，那么由 d-> e 的最优操作数，就是 k+1
  
- 是否具备重叠子问题：
  - 若是从最后一个 d -> e 时，因为之前已经算过d-> e，可以直接取到操作数

因此可以用「记忆化搜索」，自顶向下的得出答案

这道题另一个难点是：**如何定义 memo**

`memo[i][j]` 表示 ring 上的 i 位置，转动到 key 上的 j 位置，所需的最小步数

```c++
class Solution {
public:
    int ring_sz;
    int key_sz;
    vector<vector<int>> memo;                   // 定义 memo
    unordered_map<char, vector<int>> position;  // 记录字母在哪些位置上有

    int dfs(int i, int j, string &key) {  // i指向ring（当前位置），j指向key（方便找下个位置上的值）
        if (j == key_sz) return 0;        // 此时越界，所有的key都已经找全
        if (memo[i][j] != -1) return memo[i][j];

        int res = INT_MAX;
        for (int next_idx : position[key[j]]) {
            int step = abs(next_idx - i);
            int left = dfs(next_idx, j + 1, key) + step + 1;             // 往左转
            int right = dfs(next_idx, j + 1, key) + ring_sz - step + 1;  // 往右转
            res = min(res, min(left, right));
        }
        memo[i][j] = res;
        return res;
    }

    int findRotateSteps(string ring, string key) {
        ring_sz = ring.size();
        key_sz = key.size();

        for (int i = 0; i < ring_sz; i++) {
            position[ring[i]].push_back(i);
        }

        // memo[i][j] 表示 ring 上的 i 位置，转动到 key 上的 j 位置，所需的最小步数
        for (int i = 0; i < ring_sz; i++) {
            vector<int> tmp(key_sz, -1);  // -1 表示没来过
            memo.push_back(tmp);
        }

        return dfs(0, 0, key);
    }
};
```

## 方法二：动态规划

[题解来源](https://leetcode-cn.com/problems/freedom-trail/solution/freedom-trail-by-ikaruga/)

```c++
class Solution {
public:
    int findRotateSteps(string ring, string key) {
        vector<int> pos[26];
        for (int i = 0; i < ring.size(); i++) {
            pos[ring[i] - 'a'].push_back(i);
        }

        vector<vector<int>> dp(key.size(), vector<int>(ring.size(), INT_MAX));
        for (int i = 0; i < key.size(); i++) {
            for (auto j : pos[key[i] - 'a']) {
                if (i == 0) {
                    dp[i][j] = min(dp[i][j], 0 + clac(ring.size(), 0, j) + 1);
                    continue;
                }
                
                for (auto k : pos[key[i - 1] - 'a']) {
                    dp[i][j] = min(dp[i][j], dp[i - 1][k] + clac(ring.size(), k, j) + 1);
                }
            }
        }

        return *min_element(dp.back().begin(), dp.back().end());
    }

    int clac(int len, int a, int b) {
        return min((len + a - b) % len, (len + b - a) % len);
    }
};
```



