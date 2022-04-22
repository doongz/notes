# 区间DP

参考 1：[oi-wiki 区间 DP](https://oi-wiki.org/dp/interval/)

参考 2：[既是经典区间 DP，也是经典博弈论](https://mp.weixin.qq.com/s?__biz=MzU4NDE3MTEyMA==&mid=2247489400&idx=1&sn=0b629d3669329a6bf4f6ec71c2571ce7&chksm=fd9cbc67caeb357132fe0a1ca6240e2183748d94039100f539193d3eeb1dc223e0ddd4aa9584&token=2094656911&lang=zh_CN#rd)

参考 3：[石子游戏：对于先手玩家，有两种拿法](https://leetcode-cn.com/problems/stone-game/solution/shi-zi-you-xi-dong-tai-gui-hua-qu-jian-d-5ra8/)

## 概念

区间类动态规划是线性动态规划的扩展，它在分阶段地划分问题时，与阶段中元素出现的顺序和由前一阶段的哪些元素合并而来有很大的关系。

令状态 f(left, right) 表示将下标位置 left 到 right 的所有元素合并能获得的价值的最大值，cost 为将这两组元素合并起来的代价，那么
$$
f(left, right) = max(f(left, k),f(k+1,right)) + cost \ \ \ \ \ \ k\in[left,right]
$$
区间 DP 的特点：

**合并**：即将两个或多个部分进行整合，当然也可以反过来；

**特征**：能将问题分解为能两两合并的形式；

**求解**：对整个问题设最优值，**枚举合并点，将问题分解为左右两个部分**，最后合并两个部分的最优值得到原问题的最优值。

## 经典例题

[877. 石子游戏](https://leetcode-cn.com/problems/stone-game/)

亚历克斯和李用几堆石子在做游戏。偶数堆石子排成一行，每堆都有正整数颗石子 piles[i] 。

游戏以谁手中的石子最多来决出胜负。石子的总数是奇数，所以没有平局。

亚历克斯和李轮流进行，亚历克斯先开始。 每回合，玩家从行的开始或结束处取走整堆石头。 这种情况一直持续到没有更多的石子堆为止，此时手中石子最多的玩家获胜。

假设亚历克斯和李都发挥出最佳水平，当亚历克斯赢得比赛时返回 true ，当李赢得比赛时返回 false 。

```
输入：piles = [5,3,4,5]
输出：true
解释：
Alice 先开始，只能拿前 5 颗或后 5 颗石子 。
假设他取了前 5 颗，这一行就变成了 [3,4,5] 。
如果 Bob 拿走前 3 颗，那么剩下的是 [4,5]，Alice 拿走后 5 颗赢得 10 分。
如果 Bob 拿走后 5 颗，那么剩下的是 [3,4]，Alice 拿走后 4 颗赢得 9 分。
这表明，取前 5 颗石子对 Alice 来说是一个胜利的举动，所以返回 true 。
```

提示：

- 2 <= piles.length <= 500
- piles.length 是偶数。
- 1 <= piles[i] <= 500
- sum(piles) 是奇数。

### 解题步骤

**定义 `dp[left][right]` 为考虑区间 [left, right] ，在双方都做最好选择的情况下，先手与后手的最大得分差值为多少。**

那么 `dp[0][n-1]` 为考虑所有石子，先手与后手的得分差值：

- `dp[0][n-1]` > 0，则先手必胜，返回 `True`
- `dp[0][n-1]` < 0，则先手必败，返回 `False`

不失一般性的考虑 `dp[left][right]` 如何转移。根据题意，只能从两端取石子，共两种情况：

- 从左端取石子，价值为 `piles[left]`；先手取完石子后，**会导致下次变为后手**，由先后变成后手损失的值就是「先手与后手的最大得分差值」`dp[left+1][right]`。**因此本次先手从左端点取石子的话，双方差值为**：

$$
a = piles[left] - dp[left+1][right]
$$

- 从右端取石子，价值为 `piles[right]`；同理由先后变成后手损失的值为 `dp[left][right-1]`。**因此本次先手从右端点取石子的话，双方差值为**：

$$
b = piles[right] - dp[left][right-1]
$$

双方都想赢，都会做最优决策（即使自己与对方分差最大）。因此 `dp[left][right]` 为**上述两种情况中的最大值**
$$
dp[left][right] = max(a,b)
$$
根据状态转移方程，我们发现大区间的状态值依赖于小区间的状态值，典型的区间 DP 问题。

**初始化**：当只有一个数时 `dp[i][i]`，此时先手的必赢，所以 `dp[i][i] = piles[i]`

**如何遍历「经典写法，一定要会」**：对于区间 `dp[left][right]` 来说，将 `left` 从 `n - 1` 往前遍历到 `0`，而 `right` 从 `left` 位置往后遍历到 `n-1`，这样能够方便 `left < right`，将大区间划分成小区间。从小区间开始判断，不断的扩大我们的判断范围看会不会赢

时间复杂度：`O(n^2)`

空间复杂度：`O(n^2)`

```c++
class Solution {
public:
    bool stoneGame(vector<int>& piles) {
        int n = piles.size();
        vector<vector<int>> dp(n, vector<int>(n));

        // 初始化 dp 数组
        for (int i = 0; i < n; i++) {
            dp[i][i] = piles[i];
        }
        // 状态更新
        for (int left = n - 1; left >= 0; left--) {
            for (int right = left + 1; right < n; right++) {
                int a = piles[left] - dp[left + 1][right];
                int b = piles[right] - dp[left][right - 1];
                dp[left][right] = max(a, b);
            }
        }
        return dp[0][n - 1] > 0;
    }
};

```

此题还有「博弈论」的解法：先手的人必然获胜