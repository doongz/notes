题目：[115. 不同的子序列](https://leetcode-cn.com/problems/distinct-subsequences/)

给定一个字符串 `s` 和一个字符串 `t` ，计算在 `s` 的子序列中 `t` 出现的个数。

字符串的一个 **子序列** 是指，通过删除一些（也可以不删除）字符且不干扰剩余字符相对位置所组成的新字符串。（例如，`"ACE"` 是 `"ABCDE"` 的一个子序列，而 `"AEC"` 不是）

题目数据保证答案符合 32 位带符号整数范围。

```
示例 1：

输入：s = "rabbbit", t = "rabbit"
输出：3
解释：
如下图所示, 有 3 种可以从 s 中得到 "rabbit" 的方案。
rabbbit
rabbbit
rabbbit
示例 2：

输入：s = "babgbag", t = "bag"
输出：5
解释：
如下图所示, 有 5 种可以从 s 中得到 "bag" 的方案。 
babgbag
babgbag
babgbag
babgbag
babgbag

```

**提示：**

- `0 <= s.length, t.length <= 1000`
- `s` 和 `t` 由英文字母组成

## 方法一：dfs（超时）

抓住 “选”，s 要照着 t 来挑选，逐字符考察选或不选，分别来到什么状态？

可以从后往前，也可以从前往后

根据「当前比较字符」是否相同，有两大类方案

1、**末尾字符相同**，如 s 为babgbag，t 为bag，，于是 s 有两种选择：

- 用s[s.length-1]去匹配掉t[t.length-1]，问题规模缩小：继续考察babgba和ba
- 虽然当前位置可以匹配掉，但也可以不去匹配，用s前面的匹配，于是在babgba中继续挑，考察babgba和bag

2、**末尾字符不相同**，对于 s 只有一种选择：

- 当前位置不可匹配，用 s 前面的匹配



**53 / 64** 个通过测试用例

```c++
class Solution {
public:
    string _s;
    string _t;

    // 从开头到s[i]的子串中，出现『从开头到t[j]的子串』的次数
    int dfs(int i, int j) {
        // base case 这两个base case 的顺序不能调换！因为 i<0 且 j<0 时 应该返回1
        if (j < 0) return 1;
        if (i < 0) return 0;

        int res = 0;
        if (_s[i] == _t[j]) {          // 当前位置可以匹配
            res += dfs(i - 1, j - 1);  // _s[i] 消耗掉 _t[j]
            res += dfs(i - 1, j);      // 当前_s[i]不消耗  用前面的_s[i-1]消耗掉 _t[j]
        } else {                       // 当前位置不可以匹配
            res += dfs(i - 1, j);
        }
        return res;
    }

    int numDistinct(string s, string t) {
        _s = s;
        _t = t;
        return dfs(s.size() - 1, t.size() - 1);
    }
};
```

## 方法二：记忆化搜索（自顶向下）

普通 dfs 超时的原因，重复的检查了一些子问题，看下这个子问题的构成：`s[0:i] 匹配 t[0:j]`

因此使用「二维数组」描述这个子问题，`memo[i][j]` 表示 `s[0:i] 匹配 t[0:j]` 的方案数

```c++
class Solution {
public:
    string _s;
    string _t;

    int dfs(int i, int j, vector<vector<int>> &memo) {
        if (j < 0) return 1;
        if (i < 0) return 0;

        if (memo[i][j] != -1) return memo[i][j];

        int res = 0;
        if (_s[i] == _t[j]) {
            res += dfs(i - 1, j - 1, memo);
            res += dfs(i - 1, j, memo);
        } else {
            res += dfs(i - 1, j, memo);
        }
        memo[i][j] = res;
        return res;
    }

    int numDistinct(string s, string t) {
        _s = s;
        _t = t;
        int n = s.size();
        int m = t.size();
        vector<vector<int>> memo(n, vector<int>(m, -1));

        return dfs(n - 1, m - 1, memo);
    }
};
```

## 方法三：动态规划（自底向上）

看下 base case 是否确定

- 当指向 t 字符串的指针 j 位于 -1 的位置上时，表明 t 已经匹配完了，方案数为 1
- 当指向 s 字符串的指针 i 位于 -1 的位置上时，表明 s 都消耗完了，t还没匹配完，方案数为 0
- 特例，i 和 j 都位于 -1 位置上，表明 s 和 t 刚好匹配完，方案数为 1

由于下标 -1 的使用会造成数组越界，因此将 `dp[][]` 数组的两个维度都多申请一位，即 `dp[n+1][m+1]`

- t 已经匹配完，j = 0 时，`dp[i][0]=1`  
- s 已经消耗完，i = 0 时，`dp[0][j]=0`  
- 特例，i = j = 0 时，`dp[0][0]=1`  

**因此可以从base case 出发，通过在dp数组记录中间结果，「自底向上」的解决问题**

> 有个操蛋的用例，会导致中间值溢出，long long 也不行，% INT_MAX 可避免

```c++
class Solution {
public:
    int numDistinct(string s, string t) {
        int n = s.size();
        int m = t.size();
        vector<vector<long long>> dp(n + 1, vector<long long>(m + 1, 0));
        for (int i = 0; i < n; i++) {
            dp[i][0] = 1;
        }

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (j > i) continue;  // 可以做剪枝，但对效率没多大提升
                if (s[i] == t[j]) {
                    dp[i + 1][j + 1] = (dp[i][j] + dp[i][j + 1]) % INT_MAX;
                } else {
                    dp[i + 1][j + 1] = dp[i][j + 1];
                }
            }
        }
        return dp[n][m];
    }
};
```

