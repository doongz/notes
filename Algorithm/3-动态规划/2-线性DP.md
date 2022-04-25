# 线性 DP

参考 1：[动态规划 —— 线性 DP](https://blog.csdn.net/u011815404/article/details/81870275)

参考 2：[leetcode 300 题解（LIS）](https://leetcode-cn.com/problems/longest-increasing-subsequence/solution/dong-tai-gui-hua-er-fen-cha-zhao-tan-xin-suan-fa-p/)

参考 3：[leetcode 1143 题解（LCS）](https://leetcode-cn.com/problems/longest-common-subsequence/solution/fu-xue-ming-zhu-er-wei-dong-tai-gui-hua-r5ez6/)

参考 4：[LCS 问题与 LIS 问题的相互关系，以及 LIS 问题的最优解证明](https://mp.weixin.qq.com/s?__biz=MzU4NDE3MTEyMA==&mid=2247487814&idx=1&sn=e33023c2d474ff75af83eda1c4d01892&chksm=fd9cba59caeb334f1fbfa1aefd3d9b2ab6abfccfcab8cb1dbff93191ae9b787e1b4681bbbde3&token=252055586&lang=zh_CN#rd)

参考 5：[详解最长公共子序列问题，秒杀三道动态规划题目](https://mp.weixin.qq.com/s/ZhPEchewfc03xWv9VP3msg)

参考 6：[动态规划套路：最大子数组和](https://mp.weixin.qq.com/s/nrULqCsRsrPKi3Y-nUfnqg)

线性动态规划，是较常见的一类动态规划问题，其是在线性结构上进行状态转移，这类问题不像背包问题、区间DP等有固定的模板。

线性动态规划的目标函数为特定变量的线性函数，约束是这些变量的线性不等式或等式，目的是求目标函数的最大值或最小值。

因此，除了少量问题（如：LIS、LCS、LCIS等）有固定的模板外，大部分都要根据实际问题来推导得出答案。

## 一、子序列类型问题

### 1、最长上升子序列（LIS）

最长递增子序列（Longest Increasing Subsequence，简写 LIS）是非常经典的一个算法问题，比较容易想到的是动态规划解法，时间复杂度 O(N^2)，我们借这个问题来由浅入深讲解如何找状态转移方程，如何写出动态规划解法。比较难想到的是利用二分查找，时间复杂度是 O(NlogN)

题目：[300. 最长递增子序列](https://leetcode-cn.com/problems/longest-increasing-subsequence/)

给你一个整数数组 `nums` ，找到其中最长严格递增子序列的长度。

```
输入：nums = [10,9,2,5,3,7,101,18]
输出：4
解释：最长递增子序列是 [2,3,7,101]，因此长度为 4 。

输入：nums = [0,1,0,3,2,3]
输出：4

输入：nums = [7,7,7,7,7,7,7]
输出：1
```

> 「子序列」是由数组派生而来的序列，删除（或不删除）数组中的元素而不改变其余元素的顺序。「子串」一定是连续的。
>
> 例如，`[3,6,2,7]` 是数组 `[0,3,1,6,2,2,7]` 的子序列

#### 1）暴力解法

使用「回溯搜索算法」或者「位运算」的技巧，可以得到输入数组的所有子序列，时间复杂度为 O(2^N)。再对这些子串再依次判定是否为「严格上升」，时间复杂度 为O(N)，所以总的时间复杂度为：O(N 2^N)

如果题目问所有解，应该使用回溯算法（暴力搜索）搜索所有具体解。若问最优解的长度，用动态规划

#### 2）动态规划

基于「动态规划」的状态设计需要满足「无后效性」的设计思想，可以将状态定义为「以 `nums[i]` 结尾 的「上升子序列」的长度」。

> 「无后效性」的设计思想：让不确定的因素确定下来，以保证求解的过程形成一个逻辑上的有向无环图。这题不确定的因素是某个元素是否被选中，而我们设计状态的时候，让 nums[i] 必需被选中，这一点是「让不确定的因素确定下来」，也是我们这样设计状态的原因。

**1. 定义状态**：

`dp[i]` 表示：**以 `nums[i]` 结尾** 的「上升子序列」的长度。注意：这个定义中 **`nums[i]` 必须被选取，且必须是这个子序列的最后一个元素**；

**2. 状态转移方程**：

如果一个较大的数接在较小的数后面，就会形成一个更长的子序列。只要 nums[i] 严格大于在它位置之前的某个数，那么 nums[i] 就可以接在这个数后面形成一个更长的上升子序列。

$$
dp[i] = max(dp[i],\ dp[j]+1) \qquad j\in[0,i), \ nums[j] <nums[i]
$$
**3. 初始化**：

`dp[i] = 1`，11 个字符显然是长度为 11 的上升子序列。

**4. 输出**：

不能返回最后一个状态值，最后一个状态值只表示以 `nums[len - 1]` 结尾的「上升子序列」的长度，状态数组 `dp` 的最大值才是题目要求的结果。
$$
max(dp[i]) \qquad i\in[0,n-1]
$$
**5. 空间优化**：

遍历到一个新数的时候，之前所有的状态值都得保留，因此无法优化空间。

**复杂度分析**：

时间复杂度：`O(N^2)`

空间复杂度：`O(N)`

```c++
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        int n = nums.size();

        vector<int> dp(n, 1);
        for (int i = 1; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (nums[i] > nums[j]) {
                    dp[i] = max(dp[i], dp[j] + 1);
                }
            }
        }
        return *max_element(dp.begin(), dp.end());
    }
};
```

#### 3）二分查找 + 贪心算法

**状态设计思想**：

依然着眼于某个上升子序列的「结尾的元素」，**如果已经得到的上升子序列的「结尾的数越小」，那么遍历的时候后面接上一个数，会有更大的可能构成一个长度更长的上升子序列**。既然结尾越小越好，我们可以记录 在长度固定的情况下，结尾最小的那个元素的数值，这样定义以后容易得到「状态转移方程」

为了与「方法二」的状态定义区分，将状态数组命名为 tail

**1 .定义新状态**：

`tail[i]` 表示：长度为 `i + 1` 的 **所有** 上升子序列的结尾的最小值

说明：

- 数组 tail 不是问题中的「最长上升子序列」（下文还会强调），不能命名为 LIS。数组 tail 只是用于求解 LIS 问题的状态数组；
- tail[0] 表示长度为 1 的所有上升子序列中，结尾最小的元素的数值。以题目中的示例为例 [10, 9, 2, 5, 3, 7, 101, 18] 中，容易发现长度为 2 的所有上升子序列中，结尾最小的是子序列 [2, 3] ，因此 tail[1] = 3；
- 下标和长度有数值为 1 的偏差；

状态定义其实也描述了状态转移方程

**2. 状态转移方程**：

从直觉上看，**数组 `tail` 是一个严格上升数组**。下面是证明

**证明**：即对于任意的下标 `0 <= i < j < len` ，都有 `tail[i] < tail[j]`

使用反证法：假设对于任意的下标 `i` < `j` ，存在某个 `tail[i] >= tail[j]`

对于此处的 tail[i] 而言，对应一个上升子序列 [a_0, a_1, ..., a_i]，依据定义 `tail[i] = a_i`

对于此处的 tail[j] 而言，对应一个上升子序列 [b_0, b_1, ..., b_i, ... , b_j]，依据定义 `tail[j] = b_j`

由于 `tail[i] >= tail[j]`，等价于 `a_i >= b_j`，而在上升子序列 [b_0, b_1, ..., b_i, ... , b_j] 中，`b_i` 严格小于 `b_j` ，故有 `a_i >= b_j > b_i`

则上升子序列 [b_0, b_1, ..., b_i] 是一个长度也为 `i + 1` 但是结尾更小的数组，与 `a_i` 的最小性矛盾

因此原命题成立（证闭）

---

**因此只需要维护状态数组 `tail` 的定义，它的长度就是最长上升子序列的长度**。下面说明在遍历中，如何维护状态数组 `tail` 的定义

1. 在遍历数组 nums 的过程中，看到一个新数 num，如果这个数「严格大于」有序数组 tail 的最后一个元素，就把 num 放在有序数组 tail 的后面，否则进入第 2 点；
2. 在有序数组 `tail` 中查找第 1 个等于大于 `num` 的那个数，试图让它变小；
   - 如果有序数组 `tail` 中存在 **等于** `num` 的元素，什么都不做，因为以 `num` 结尾的最短的「上升子序列」已经存在；
   - 如果有序数组 `tail` 中存在 **大于** `num` 的元素，找到第 1 个，让它变小，这样我们就找到了一个 **结尾更小**的**相同长度**的上升子序列。

说明：

- 我们再看一下数组 tail[i] 的定义：长度为 i + 1 的 **所有** 最长上升子序列的结尾的最小值。因此，在遍历的过程中，我们会不断的刷新 tail 数组，使其整体上变小，最后位置上的数也变小，**以便让新来的数扩充 tail 数组**
- 这一步可以认为是「贪心算法」，总是做出在当前看来最好的选择，当前「最好的选择」是：当前只让让第 1 个严格大于 nums[i] 的数变小，变成 nums[i]，这一步操作是「无后效性」的；
- 由于是在有序数组中的操作，因此可以使用「二分查找算法」。

**3. 初始化**：

遍历第 1 个数 `nums[0]`，直接放在有序数组 `tail` 的开头 `tail[0] = nums[0]`

**4. 输出**：

有序数组 `tail` 的长度，就是所求的「最长上升子序列」的长度

**5. 空间优化**：

无法优化空间

**复杂度分析**：

时间复杂度：`O(Nlog N)`

空间复杂度：`O(N)`

```c++
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        vector<int> tail;
        tail.push_back(nums[0]);
        for (int i = 1; i < nums.size(); i++) {
            int end = *tail.rbegin();
            if (nums[i] > end) {
                tail.push_back(nums[i]);
            } else if (nums[i] == end) {
                continue;
            } else if (nums[i] < end) {
                auto it = lower_bound(tail.begin(), tail.end(), nums[i]);
                *it = nums[i];
            }
        }
        return tail.size();
    }
};
```

### 2、最长公共子序列（LCS）

计算最长公共子序列（Longest Common Subsequence，简称 LCS）是一道经典的动态规划题目

题目：[1143. 最长公共子序列](https://leetcode-cn.com/problems/longest-common-subsequence/)

给定两个字符串 text1 和 text2，返回这两个字符串的最长 公共子序列 的长度。如果不存在 公共子序列 ，返回 0 。

一个字符串的 子序列 是指这样一个新的字符串：它是由原字符串在不改变字符的相对顺序的情况下删除某些字符（也可以不删除任何字符）后组成的新字符串。

```
输入：text1 = "abcde", text2 = "ace" 
输出：3  
解释：最长公共子序列是 "ace" ，它的长度为 3 。

输入：text1 = "abc", text2 = "abc"
输出：3
解释：最长公共子序列是 "abc" ，它的长度为 3 。

输入：text1 = "abc", text2 = "def"
输出：0
解释：两个字符串没有公共子序列，返回 0 。
```

#### 1）动态规划

动态规划是有套路的：

- 单个数组或者字符串要用动态规划时，可以把动态规划 `dp[i]` 定义为 `nums[0:i]` 中想要求的结果；
- 当两个数组或者字符串要用动态规划时，可以把动态规划定义成两维的 `dp[i][j]` ，其含义是在 `A[0:i]` 与 `B[0:j]` 之间匹配得到的想要的结果。

**1. 状态定义**

对于本题，定义 `dp[i][j]` 表示 `text1[0:i-1]` 和 `text2[0:j-1]` 的最长公共子序列 

> 注：`text1[0:i-1]` 表示的是 text1 的 第 0 个元素到第 i - 1 个元素，两端都包含

之所以 `dp[i][j]` 的定义不是 `text1[0:i]` 和 `text2[0:j]` ，是为了方便当 i = 0 或者 j = 0 的时候，`dp[i][j]` 表示的为空字符串和另外一个字符串的匹配，这样 `dp[i][j]` 可以初始化为 0

**2. 状态转移方程**

- 当 `text1[i - 1] == text2[j - 1]` 时，说明两个子字符串的最后一位相等，所以最长公共子序列又增加了 1，所以 `dp[i][j] = dp[i - 1][j - 1] + 1`；举个例子，比如对于 ac 和 bc 而言，他们的最长公共子序列的长度等于 a 和 b 的最长公共子序列长度 0 + 1 = 1

- 当 `text1[i - 1] != text2[j - 1]` 时，说明两个子字符串的最后一位不相等，那么此时的状态 `dp[i][j]` 应该是 `dp[i - 1][j]` 和 `dp[i][j - 1]` 的最大值。举个例子，比如对于 ace 和 bc 而言，他们的最长公共子序列的长度等于 ① ace 和 b 的最长公共子序列长度0 与 ② ac 和 bc 的最长公共子序列长度1 的最大值，即 1

> 选择 `dp[i - 1][j]` 和 `dp[i][j - 1]` 中最大值的合理性在于：我们需要在 `d[i][j]`  这个位置上选择一个字母（来自于 `text1[i-1]`、`text2[j-1]`）作为结尾，必然希望这个字母代表的子字符串最长，那么后面的计算才能基于最优的子问题

$$
dp[i][j] = 
\begin{cases}
dp[i-1][j-1]+1 & text1[i-1]=text2[j-1] \\ \\
max(dp[i-1][j], \ dp[i][j-1]) & text1[i-1]\neq text2[j-1]
\end{cases}
$$

**3. 状态的初始化**

初始化就是要看当 i = 0 与 j = 0 时，`dp[i][j]` 应该取值为多少。

当 i = 0 时，`dp[0][j]` 表示的是 text1 中取空字符串 跟 text2 的最长公共子序列，结果肯定为 0.

当 j = 0 时，`dp[i][0]` 表示的是 text2 中取空字符串 跟 text1 的最长公共子序列，结果肯定为 0.

综上，当 i = 0 或者 j = 0 时，`dp[i][j]` 初始化为 0.

**4. 遍历方向与范围**

由于 `dp[i][j]` 依赖与 `dp[i - 1][j - 1]` , `dp[i - 1][j]`, `dp[i][j - 1]`，所以 i 和 j 的遍历顺序肯定是从小到大的。

另外，由于当 i 或 j 取值为 0 的时候，`dp[i][j] = 0`，而 dp 数组本身初始化就是为 0，所以，直接让 i 和 j 从 1 开始遍历。遍历的结束应该是字符串的长度为 len(text1) 和 len(text2)

**5. 最终返回结果**

由于 `dp[i][j]` 的含义是 `text1[0:i-1]` 和 `text2[0:j-1]` 的最长公共子序列。我们最终希望求的是 text1 和 text2 的最长公共子序列。所以需要返回的结果是 i = len(text1) 并且 j = len(text2) 时的 `dp[len(text1)][len(text2)]`

**复杂度分析**：

时间复杂度：`O(MN)`

空间复杂度：`O(MN`

```c++
class Solution {
public:
    int longestCommonSubsequence(string text1, string text2) {
        int n = text1.size();
        int m = text2.size();
        vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
        for (int i = 1; i < n + 1; i++) {
            for (int j = 1; j < m + 1; j++) {
                if (text1[i - 1] == text2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = max(dp[i][j - 1], dp[i - 1][j]);
                }
            }
        }
        return dp[n][m];
    }
};
```









## 例题

| 题目                                                         | 题解                                                         | 难度 | 推荐指数 |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- | -------- |
| [10. 正则表达式匹配](https://leetcode-cn.com/problems/regular-expression-matching) | [LeetCode 题解链接](https://leetcode-cn.com/problems/regular-expression-matching/solution/shua-chuan-lc-dong-tai-gui-hua-jie-fa-by-zn9w/) | 困难 | 🤩🤩🤩🤩     |
| [44. 通配符匹配](https://leetcode-cn.com/problems/wildcard-matching/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/wildcard-matching/solution/gong-shui-san-xie-xiang-jie-dong-tai-gui-ifyx/) | 困难 | 🤩🤩🤩🤩     |
| [45. 跳跃游戏 II](https://leetcode-cn.com/problems/jump-game-ii/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/jump-game-ii/solution/xiang-jie-dp-tan-xin-shuang-zhi-zhen-jie-roh4/) | 中等 | 🤩🤩🤩🤩     |
| [91. 解码方法](https://leetcode-cn.com/problems/decode-ways/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/decode-ways/solution/gong-shui-san-xie-gen-ju-shu-ju-fan-wei-ug3dd/) | 中等 | 🤩🤩🤩      |
| [115. 不同的子序列](https://leetcode-cn.com/problems/distinct-subsequences/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/distinct-subsequences/solution/xiang-jie-zi-fu-chuan-pi-pei-wen-ti-de-t-wdtk/) | 困难 | 🤩🤩🤩🤩     |
| [119. 杨辉三角 II](https://leetcode-cn.com/problems/pascals-triangle-ii/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/pascals-triangle-ii/solution/dong-tai-gui-hua-luo-ti-chang-jian-de-ko-n2xj/) | 简单 | 🤩🤩🤩      |
| [213. 打家劫舍 II](https://leetcode-cn.com/problems/house-robber-ii/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/house-robber-ii/solution/gong-shui-san-xie-ru-he-jiang-xin-xian-z-zf0w/) | 中等 | 🤩🤩🤩      |
| [338. 比特位计数](https://leetcode-cn.com/problems/counting-bits/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/counting-bits/solution/po-su-jie-fa-dong-tai-gui-hua-jie-fa-by-vvail/) | 简单 | 🤩🤩🤩      |
| [403. 青蛙过河](https://leetcode-cn.com/problems/frog-jump/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/frog-jump/solution/gong-shui-san-xie-yi-ti-duo-jie-jiang-di-74fw/) | 困难 | 🤩🤩🤩      |
| [576. 出界的路径数](https://leetcode-cn.com/problems/out-of-boundary-paths/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/out-of-boundary-paths/solution/gong-shui-san-xie-yi-ti-shuang-jie-ji-yi-asrz/) | 中等 | 🤩🤩🤩🤩     |
| [639. 解码方法 II](https://leetcode-cn.com/problems/decode-ways-ii/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/decode-ways-ii/solution/gong-shui-san-xie-fen-qing-kuang-tao-lun-902h/) | 困难 | 🤩🤩🤩🤩     |
| [650. 只有两个键的键盘](https://leetcode-cn.com/problems/2-keys-keyboard/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/2-keys-keyboard/solution/gong-shui-san-xie-yi-ti-san-jie-dong-tai-f035/) | 中等 | 🤩🤩🤩🤩     |
| [678. 有效的括号字符串](https://leetcode-cn.com/problems/valid-parenthesis-string/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/valid-parenthesis-string/solution/gong-shui-san-xie-yi-ti-shuang-jie-dong-801rq/) | 中等 | 🤩🤩🤩🤩🤩    |
| [688. 骑士在棋盘上的概率](https://leetcode-cn.com/problems/knight-probability-in-chessboard/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/knight-probability-in-chessboard/solution/gong-shui-san-xie-jian-dan-qu-jian-dp-yu-st8l/) | 中等 | 🤩🤩🤩🤩🤩    |
| [1137. 第 N 个泰波那契数](https://leetcode-cn.com/problems/n-th-tribonacci-number/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/n-th-tribonacci-number/solution/gong-shui-san-xie-yi-ti-si-jie-die-dai-d-m1ie/) | 简单 | 🤩🤩🤩🤩     |
| [1220. 统计元音字母序列的数目](https://leetcode-cn.com/problems/count-vowels-permutation/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/count-vowels-permutation/solution/gong-shui-san-xie-yi-ti-shuang-jie-xian-n8f4o/) | 困难 | 🤩🤩🤩🤩     |
| [1751. 最多可以参加的会议数目 II](https://leetcode-cn.com/problems/maximum-number-of-events-that-can-be-attended-ii/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/maximum-number-of-events-that-can-be-attended-ii/solution/po-su-dp-er-fen-dp-jie-fa-by-ac_oier-88du/) | 困难 | 🤩🤩🤩      |
| [1787. 使所有区间的异或结果为零](https://leetcode-cn.com/problems/make-the-xor-of-all-segments-equal-to-zero/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/make-the-xor-of-all-segments-equal-to-zero/solution/gong-shui-san-xie-chou-xiang-cheng-er-we-ww79/) | 困难 | 🤩🤩🤩🤩     |
| [剑指 Offer 10- I. 斐波那契数列](https://leetcode-cn.com/problems/fei-bo-na-qi-shu-lie-lcof/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/fei-bo-na-qi-shu-lie-lcof/solution/gong-shui-san-xie-yi-ti-si-jie-dong-tai-9zip0/) | 简单 | 🤩🤩🤩🤩🤩    |
| [剑指 Offer 42. 连续子数组的最大和](https://leetcode-cn.com/problems/lian-xu-zi-shu-zu-de-zui-da-he-lcof/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/lian-xu-zi-shu-zu-de-zui-da-he-lcof/solution/gong-shui-san-xie-jian-dan-xian-xing-dp-mqk5v/) | 简单 | 🤩🤩🤩🤩🤩    |
| [LCP 07. 传递信息](https://leetcode-cn.com/problems/chuan-di-xin-xi/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/chuan-di-xin-xi/solution/gong-shui-san-xie-tu-lun-sou-suo-yu-dong-cyxo/) | 简单 | 🤩🤩🤩🤩     |

