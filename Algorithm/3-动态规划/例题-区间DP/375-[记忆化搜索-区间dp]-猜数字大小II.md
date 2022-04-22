[375. 猜数字大小 II](https://leetcode-cn.com/problems/guess-number-higher-or-lower-ii/)

## 方法一：记忆化搜索

设计递归函数为 `int dfs(int left, int right)` 传入参数 left 和 right 代表在范围 [left, right] 内进行猜数，返回值为在 [left, right] 内猜中数字至少需要多少钱。

我们可决策的部分为「选择猜哪个数 x」，而不可决策的是「选择某个数 x 之后（假设没有猜中），真实值会落在哪边」。

**确保你获胜** 的最小现金数，**不管我选择那个数字**：

- 「确保+不管」，是要选择当前节点下左右分支的「最大值」，才能「确保+不管」那些小的值都能取到，因此分支比较用 max
- 「最小」，是要选择所有可能的结点值下，有一个结果即可，因此用 min

```c++
class Solution {
public:
    int memo[201][201];
    int dfs(int left, int right) {
        if (left >= right) return 0;  // base case
        if (memo[left][right] != 0) return memo[left][right];

        int res = INT_MAX;
        for (int val = left; val <= right; val++) {
            int sub_left = dfs(left, val - 1);
            int sub_right = dfs(val + 1, right);
            int max_sub = max(sub_left, sub_right) + val;
            res = min(res, max_sub);
        }
        memo[left][right] = res;
        return res;
    }

    int getMoneyAmount(int n) {
        return dfs(1, n);
    }
};
```

## 方法二：区间DP

通过「记忆化搜索」的递归过程，我们发现，在求解 [i, j] 的最小成本时，需要依赖于 [i, k - 1] 和 [k + 1, j] 这样的比 [i, j] 更小的区间。

这引导我们使用「区间 DP」进行求解

**定义状态数组和状态**：`dp[i][j]` 为区间 [i, j] 内进行猜数的最小成本

**状态方程**：结合【确保你获胜的最小现金数】这个条件
$$
f(i,j) = \min\limits_{i<=k<=j}\{max(f(i,k-1),f(k+1,j)+k)\}
$$
最终的 `dp[i][j]` 为所有可选的数值 `k` 中的最小值

时间复杂度：`O(n^3)`

空间复杂度：`O(n^2)`

```c++
class Solution {
public:
    int getMoneyAmount(int n) {
        // 初始化动态数组
        vector<vector<int>> dp(n + 2, vector<int>(n + 2));

        // 区间dp的常用遍历方法，可确保left<right
        for (int left = n - 1; left >= 1; left--) {
            for (int right = left + 1; right <= n; right++) {
                int tmp = INT_MAX;
                for (int k = left; k <= right; k++) {
                    tmp = min(tmp, max(dp[left][k - 1], dp[k + 1][right]) + k);
                }
                dp[left][right] = tmp;
            }
        }
        return dp[1][n];
    }
};
```

```
问：为什么在循环中 int left = n - 1、int right = left + 1？
答：注意，right不可与left重合，因为重合时left=right=k，dp[k][k]将会等于k，而dp[k][k]根据题意初始时为0，且之后状态不会刷新

问：动态数组的size为n+2？
答：首先+1是因为，我们使用数组的范围是[1,n]，因此申请n+1个位置
再+1是因为，在第三个循环会使 k=right，而且需要使用dp[k+1]，right所使用的范围是[1,n]，那么 k+1=right+1 所使用的范围是[1,n+1]
因此，需要动态数组的size为n+2
```

