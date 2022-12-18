[514. 自由之路](https://leetcode-cn.com/problems/freedom-trail/)

电子游戏“辐射4”中，任务 **“通向自由”** 要求玩家到达名为 “**Freedom Trail Ring”** 的金属表盘，并使用表盘拼写特定关键词才能开门。

给定一个字符串 `ring` ，表示刻在外环上的编码；给定另一个字符串 `key` ，表示需要拼写的关键词。您需要算出能够拼写关键词中所有字符的**最少**步数。

最初，**ring** 的第一个字符与 `12:00` 方向对齐。您需要顺时针或逆时针旋转 `ring` 以使 **key** 的一个字符在 `12:00` 方向对齐，然后按下中心按钮，以此逐个拼写完 **`key`** 中的所有字符。

旋转 `ring` 拼出 key 字符 `key[i]` 的阶段中：

1. 您可以将 **ring** 顺时针或逆时针旋转 **一个位置** ，计为1步。旋转的最终目的是将字符串 **`ring`** 的一个字符与 `12:00` 方向对齐，并且这个字符必须等于字符 **`key[i]` 。**
2. 如果字符 **`key[i]`** 已经对齐到12:00方向，您需要按下中心按钮进行拼写，这也将算作 **1 步**。按完之后，您可以开始拼写 **key** 的下一个字符（下一阶段）, 直至完成所有拼写。

**示例 1：**

![img](https://assets.leetcode.com/uploads/2018/10/22/ring.jpg)

```
输入: ring = "godding", key = "gd"
输出: 4
解释:
 对于 key 的第一个字符 'g'，已经在正确的位置, 我们只需要1步来拼写这个字符。 
 对于 key 的第二个字符 'd'，我们需要逆时针旋转 ring "godding" 2步使它变成 "ddinggo"。
 当然, 我们还需要1步进行拼写。
 因此最终的输出是 4。
```

**示例 2:**

```
输入: ring = "godding", key = "godding"
输出: 13
```

提示：

1 <= ring.length, key.length <= 100
ring 和 key 只包含小写英文字母
保证 字符串 key 一定可以由字符串  ring 旋转拼出

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



