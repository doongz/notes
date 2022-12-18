题目：[712. 两个字符串的最小ASCII删除和](https://leetcode-cn.com/problems/minimum-ascii-delete-sum-for-two-strings/)

## 方法：LCS

s1 -> 公共子串 -> s2

删除的 ascii 最小，那么保留的公共子串 ascii 最大

s1 -> 最大ascii公共子串 -> s2

**问题转化为：求最大ascii公共子串**

定义状态数组：`dp[i][j]` 表示 `s1[0:i-1]` 和 `s2[0:j-1]` 的最大ascii公共子串的ascii值

初始化：当i或j为0时，没有公共子串，此时状态为0


```c++
class Solution {
public:
    int minimumDeleteSum(string s1, string s2) {
        int n = s1.size();
        int m = s2.size();
        vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
        for (int i = 1; i < n + 1; i++) {
            for (int j = 1; j < m + 1; j++) {
                if (s1[i - 1] == s2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1] + s1[i - 1];
                } else {
                    dp[i][j] = max(dp[i][j - 1], dp[i - 1][j]);
                }
            }
        }
        // cout << dp[n][m] << endl;
        int ascii_1 = 0, ascii_2 = 0;
        for (int i = 0; i < n; i++) ascii_1 += s1[i];
        for (int j = 0; j < m; j++) ascii_2 += s2[j];
        return (ascii_1 - dp[n][m]) + (ascii_2 - dp[n][m]);
    }
};
```

