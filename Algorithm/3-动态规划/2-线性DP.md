# 线性 DP

参考：[动态规划 —— 线性 DP](https://blog.csdn.net/u011815404/article/details/81870275)

线性动态规划，是较常见的一类动态规划问题，其是在线性结构上进行状态转移，这类问题不像背包问题、区间DP等有固定的模板。

线性动态规划的目标函数为特定变量的线性函数，约束是这些变量的线性不等式或等式，目的是求目标函数的最大值或最小值。

因此，除了少量问题（如：LIS、LCS、LCIS等，提炼为序列DP）有固定的模板外，大部分都要根据实际问题来推导得出答案。

## 一、思考顺序

**1. 定义状态**

**2. 状态转移方程**

**3. 初始化**

**4. 输出**

**空间优化**

**复杂度分析**

## 二、常用的定义状态方式

dp[i] 为以 nums[i] 结尾的方案数，最后的答案可能是 dp 数组中的最大值

dp[i] 为在 [0, i] 范围内的方案数，最后的答案可能是 dp[n-1]



## 三、打家劫舍问题

### 打家劫舍 I

题目：[198. 打家劫舍](https://leetcode-cn.com/problems/house-robber/)

你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。

给定一个代表每个房屋存放金额的非负整数数组，计算你 不触动警报装置的情况下 ，一夜之内能够偷窃到的最高金额。

```
输入：[1,2,3,1]
输出：4
解释：偷窃 1 号房屋 (金额 = 1) ，然后偷窃 3 号房屋 (金额 = 3)。
     偷窃到的最高金额 = 1 + 3 = 4 。

输入：[2,7,9,3,1]
输出：12
解释：偷窃 1 号房屋 (金额 = 2), 偷窃 3 号房屋 (金额 = 9)，接着偷窃 5 号房屋 (金额 = 1)。
     偷窃到的最高金额 = 2 + 9 + 1 = 12 。
```

**1. 定义状态**

dp[i] 为在 [0, i] 范围内的偷窃最高金额

**2. 状态转移方程**

根据**当前位置 nums[i] 是否被偷盗**，分为两个子问题

1. 若当前位置 i 被偷，那么前一位置 i-1 肯定不会被偷，我们细想下这里的状态该怎样转移

是不是可以直接用 `dp[i] = dp[i-1] + nums[i]` 呢？**不行**

因为此时【位置 i 被偷】是一种假设，推导的【 i-1 不被偷】继承了假设，d[i-1] 来代表【 i-1 不被偷】是不准确的

但可以确定的是，若【 i-1 不被偷】，那么它的最高金额一定等于更前一个位置上的最高金额 dp[i-2]，**d[i-2] 来代表【 i-1 不被偷】才是准确的**，因此这种情况下 `dp[i] = dp[i-2] + nums[i]`

2. 若当前位置 i 没被偷，那么前一位置 i-1 可能会被偷，也可能没被偷

由于我们对状态的定义，dp[i-1] 天生包含了对 i-1 位置可能会被偷、也可能没被偷的统计结果，这个子问题已经被完美解决了，直接拿来用

因此，这种情况下 `dp[i] = dp[i-1]`

最后，这两个子问题再综合下，取最大值作为 [0, i] 范围内的偷窃最高金额
$$
dp[i] = max(dp[i-2]+nums[i], \ dp[i-1])
$$
**3. 初始化**

计算当前位置的时候，需要往前面看两位，因此需要初始化前面两位

dp[0] = nums[0]，有一个数的时候，只能偷这个

dp[0] = max(nums[0], nums[1])，有两个数的时候，偷最大的

**4. 输出**

dp[n-1] 为在 [0, n-1] 范围内的偷窃最高金额

**空间优化**

当前状态的计算仅与前面两位有关，可进行优化

**复杂度分析**

时间复杂度：`O(n)`

空间复杂度：`O(n)` 或`O(1)`

```c++
class Solution {
public:
    int rob(vector<int>& nums) {
        int n = nums.size();
        if (n == 1) return nums[0];
        if (n == 2) return max(nums[0], nums[1]);

        vector<int> dp(n, 0);
        dp[0] = nums[0];
        dp[1] = max(nums[0], nums[1]);

        for (int i = 2; i < n; i++) {
            dp[i] = max(dp[i - 2] + nums[i], dp[i - 1]);
        }
        return dp[n - 1];
    }
};
```

```c++
class Solution {
public:
    int rob(vector<int>& nums) {
        int n = nums.size();
        if (n == 1) return nums[0];
        if (n == 2) return max(nums[0], nums[1]);

        int prepre = nums[0];
        int pre = max(nums[0], nums[1]);
        int cur = pre;

        for (int i = 2; i < n; i++) {
            cur = max(prepre + nums[i], pre);
            prepre = pre;
            pre = cur;
        }
        return cur;
    }
};
```

### 打家劫舍 II

题目：[213. 打家劫舍 II](https://leetcode-cn.com/problems/house-robber-ii/)

你是一个专业的小偷，计划偷窃沿街的房屋，每间房内都藏有一定的现金。这个地方所有的房屋都围成一圈 ，这意味着**第一个房屋和最后一个房屋是紧挨着的**。同时，相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警 。

给定一个代表每个房屋存放金额的非负整数数组，计算你 在不触动警报装置的情况下 ，今晚能够偷窃到的最高金额。

```
输入：nums = [2,3,2]
输出：3
解释：你不能先偷窃 1 号房屋（金额 = 2），然后偷窃 3 号房屋（金额 = 2）, 因为他们是相邻的。

输入：nums = [1,2,3,1]
输出：4
解释：你可以先偷窃 1 号房屋（金额 = 1），然后偷窃 3 号房屋（金额 = 3）。
     偷窃到的最高金额 = 1 + 3 = 4 。

输入：nums = [1,2,3]
输出：3
```

这题二与题一的不同在于：是首位相连的

**1. 定义状态**

同样，dp[i] 为在 [0, i] 范围内的偷窃最高金额

**2. 状态转移方程**

除了，对根据**当前位置 nums[i] 是否被偷盗**，分为两个子问题（沿用题一）
$$
dp[i] = max(dp[i-2]+nums[i], \ dp[i-1])
$$
由于这一题「首尾相连」，因此对**是否偷第一家**，划分为「两轮状态转移」

- 若**偷第一家**，第二家必然不会被偷，第三家可偷可不偷，因此从第三家开始「正经偷」，**最后一家绝对不偷**
- 若**不偷第一家**，第二家可偷可不偷，因此从第二家开始「正经偷」，**最后一家可偷可不偷**

**3. 初始化**

按照上面对**是否偷第一家**，对「两轮状态转移」进行初始化

- 若偷第一家 `dp[0] = nums[0]`，第二家必然不会被偷 `dp[1] = dp[0]`
- 若不偷第一家 `dp[0] = 0`，第二家初始化为 `dp[1] = nums[1]`，

**4. 输出**

「两轮状态转移」结果的最大值

**空间优化**

当前状态的计算仅与前面两位有关，可进行优化

**复杂度分析**

时间复杂度：`O(n)`

空间复杂度：`O(n)` 或`O(1)`

```c++
class Solution {
public:
    int rob(vector<int>& nums) {
        int n = nums.size();
        if (n == 1) return nums[0];
        if (n == 2) return max(nums[0], nums[1]);

        vector<int> dp(n, 0);
        int res1 = 0, res2 = 0;

        // 偷第一家，最后一家绝对不偷
        dp[0] = nums[0];
        dp[1] = dp[0];
        for (int i = 2; i < n; i++) {
            if (i != n - 1) {
                dp[i] = max(dp[i - 2] + nums[i], dp[i - 1]);
            } else {
                dp[i] = dp[i - 1];
            }
        }
        res1 = dp[n - 1];

        // 不偷第一家，最后一家可偷可不偷
        dp[0] = 0;
        dp[1] = nums[1];
        for (int i = 2; i < n; i++) {
            dp[i] = max(dp[i - 2] + nums[i], dp[i - 1]);
        }
        res2 = dp[n - 1];

        return max(res1, res2);
    }
};
```

```c++
class Solution {
public:
    int rob(vector<int>& nums) {
        int n = nums.size();
        if (n == 1) return nums[0];
        if (n == 2) return max(nums[0], nums[1]);

        // 偷第一家，最后一家绝对不偷
        int prepre = nums[0];
        int pre = nums[0];
        int cur1 = pre;
        for (int i = 2; i < n; i++) {
            if (i != n - 1) {
                cur1 = max(prepre + nums[i], pre);
            } else {
                cur1 = pre;
            }
            prepre = pre;
            pre = cur1;
        }

        // 不偷第一家，最后一家可偷可不偷
        prepre = 0;
        pre = nums[1];
        int cur2 = pre;
        for (int i = 2; i < n; i++) {
            cur2 = max(prepre + nums[i], pre);
            prepre = pre;
            pre = cur2;
        }
        return max(cur1, cur2);
    }
};
```

### 打家劫舍III

解法为【树形DP】，请看[树形DP]()一文







## 例题

| 题目                                                         | 题解                                                         | 难度 | 推荐指数 |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- | -------- |
| [10. 正则表达式匹配](https://leetcode-cn.com/problems/regular-expression-matching) | [LeetCode 题解链接](https://leetcode-cn.com/problems/regular-expression-matching/solution/shua-chuan-lc-dong-tai-gui-hua-jie-fa-by-zn9w/) | 困难 | 🤩🤩🤩🤩     |
| [44. 通配符匹配](https://leetcode-cn.com/problems/wildcard-matching/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/wildcard-matching/solution/gong-shui-san-xie-xiang-jie-dong-tai-gui-ifyx/) | 困难 | 🤩🤩🤩🤩     |
|                                                              |                                                              |      |          |
|                                                              |                                                              |      |          |
|                                                              |                                                              |      |          |
|                                                              |                                                              |      |          |
|                                                              |                                                              |      |          |
|                                                              |                                                              |      |          |
|                                                              |                                                              |      |          |
|                                                              |                                                              |      |          |
|                                                              |                                                              |      |          |
|                                                              |                                                              |      |          |
|                                                              |                                                              |      |          |
|                                                              |                                                              |      |          |
|                                                              |                                                              |      |          |
|                                                              |                                                              |      |          |
| [1751. 最多可以参加的会议数目 II](https://leetcode-cn.com/problems/maximum-number-of-events-that-can-be-attended-ii/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/maximum-number-of-events-that-can-be-attended-ii/solution/po-su-dp-er-fen-dp-jie-fa-by-ac_oier-88du/) | 困难 | 🤩🤩🤩      |
| [1787. 使所有区间的异或结果为零](https://leetcode-cn.com/problems/make-the-xor-of-all-segments-equal-to-zero/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/make-the-xor-of-all-segments-equal-to-zero/solution/gong-shui-san-xie-chou-xiang-cheng-er-we-ww79/) | 困难 | 🤩🤩🤩🤩     |
|                                                              |                                                              |      |          |
|                                                              |                                                              |      |          |
|                                                              |                                                              |      |          |

