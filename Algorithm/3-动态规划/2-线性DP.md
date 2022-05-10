# 线性 DP

参考 1：[动态规划 —— 线性 DP](https://blog.csdn.net/u011815404/article/details/81870275)

参考 2：[宫水三叶 路径问题合集](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzU4NDE3MTEyMA==&action=getalbum&album_id=1773144264147812354&scene=173&from_msgid=2247485037&from_itemidx=1&count=3&nolastread=1#wechat_redirect)

线性动态规划，是较常见的一类动态规划问题，其是在线性结构上进行状态转移，这类问题不像背包问题、区间DP等有固定的模板。

线性动态规划的目标函数为特定变量的线性函数，约束是这些变量的线性不等式或等式，目的是求目标函数的最大值或最小值。

因此，除了少量问题（如：LIS、LCS、LCIS等，提炼为序列DP）有固定的模板外，大部分都要根据实际问题来推导得出答案。

**1. 我们是如何确定本题可以使用动态规划来解决的？**

通常我们要从**「有无后效性」**进行入手分析。

如果对于某个状态，我们可以只关注状态的值，而不需要关注状态是如何转移过来的话，那么这就是一个无后效性的问题，可以考虑使用 DP 解决。

另外一个更加实在的技巧，我们还可以通过 **数据范围** 来猜测是不是可以用 DP 来做。

因为 DP 是一个递推的过程，因此如果数据范围是 10^5~10^6 的话，可以考虑是不是可以使用一维 DP 来解决；如果数据范围是 10^2~10^3 的话，可以考虑是不是可以使用二维 DP 来做 ...

**2. 我们是如何确定本题的状态定义的？**

说实话，DP 的状态定义很大程度是靠经验去猜的。

虽然大多数情况都是猜的，但也不是毫无规律，相当一部分题目的状态定义是与**「结尾」**和**「答案」**有所关联的。

**3. 我们是如何确定状态转移方程的？**

通常来说，如果我们的状态定义猜对了，**「状态转移方程」**就是对**「最后一步的分情况讨论」**。

如果我们有一个对的**「状态定义」**的话，基本上**「状态转移方程」**就是呼之欲出。

因此一定程度上，**状态转移方程可以反过来验证我们状态定义猜得是否正确**：

如果猜了一个状态定义，然后发现无法列出涵盖所有情况（不漏）的状态转移方程，多半就是**状态定义猜错了，赶紧换个思路，而不是去死磕状态转移方程**。

**4. 对状态转移的要求是什么？**

我们的状态转移是要做到**「不漏」**还是**「不重不漏」**取决于问题本身：

- 如果是求最值的话，我们只需要确保**「不漏」**即可，因为重复不影响结果。
- 如果是求方案数的话，我们需要确保**「不重不漏」**。

**5. 我们是如何分析动态规划的时间复杂度的？**

对于动态规划的复杂度/计算量分析，有多少个状态，复杂度/计算量就是多少。

因此一维 DP 的复杂度通常是线性的 O(n)，而二维 DP 的复杂度通常是平方的 O(n^2)。

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



## 四、路径问题

### [62. 不同路径](https://leetcode-cn.com/problems/unique-paths/)

一个机器人位于一个 m x n 网格的左上角 （起始点在下图中标记为 “Start” ）。

机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为 “Finish” ）。

问总共有多少条不同的路径？

![62](/Users/zhangdong/Desktop/algo/Algorithm/3-动态规划/doc/62.png)

- `1 <= m, n <= 100`
- 题目数据保证答案小于等于 `2 * 10^9`

```
输入：m = 3, n = 7
输出：28

输入：m = 3, n = 2
输出：3
解释：
从左上角开始，总共有 3 条路径可以到达右下角。
1. 向右 -> 向下 -> 向下
2. 向下 -> 向下 -> 向右
3. 向下 -> 向右 -> 向下
```

**1. 定义状态**

`dp[i][j]` 为到达位置 `(i,j)` 的不同路径数量

**2. 状态转移方程**

机器人每次只能向下或者向右移动一步，表明**当前位置可能从上方或者左边走来的**

- 当前位置只能从「左边」走来，即第一行，`dp[i][j] = dp[i][j-1]`
- 当前位置只能从「上方」走来，即第一列，`dp[i][j] = dp[i-1][j]`
- 当前位置「即能从上方又能从左边」走来，`dp[i][j] = dp[i][j-1] + dp[i-1][j]`

**3. 初始化**

`dp[0][0] = 1`  起点为 1

**4. 输出**

`dp[m-1][n-1] `

**空间优化**

不优化

**复杂度分析**

时间复杂度：`O(m * n)`

空间复杂度：`O(m * n)`

```c++
class Solution {
public:
    int uniquePaths(int m, int n) {
        vector<vector<int>> dp(m, vector<int>(n, 0));
        dp[0][0] = 1;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (i == 0 && j > 0) {  // 第一行
                    dp[i][j] = dp[i][j - 1];
                } else if (i > 0 && j == 0) {  // 第一列
                    dp[i][j] = dp[i - 1][j];
                } else if (i > 0 && j > 0) {
                    dp[i][j] = dp[i][j - 1] + dp[i - 1][j];
                }
            }
        }
        return dp[m - 1][n - 1];
    }
};
```

### [63. 不同路径 II](https://leetcode-cn.com/problems/unique-paths-ii/)

一个机器人位于一个 m x n 网格的左上角 （起始点在下图中标记为 “Start” ）。

机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为 “Finish”）。

现在考虑网格中有障碍物。那么从左上角到右下角将会有多少条不同的路径？

网格中的障碍物和空位置分别用 1 和 0 来表示。

![63](/Users/zhangdong/Desktop/algo/Algorithm/3-动态规划/doc/63.png)

```
输入：obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
输出：2
解释：3x3 网格的正中间有一个障碍物。
从左上角到右下角一共有 2 条不同的路径：
1. 向右 -> 向右 -> 向下 -> 向下
2. 向下 -> 向下 -> 向右 -> 向右

输入：obstacleGrid = [[0,1],[0,0]]
输出：1
```

**1. 定义状态**

与上题一样，`dp[i][j]` 为到达位置 `(i,j)` 的不同路径数量

**2. 状态转移方程**

与上题的不同：有障碍物，表明当前位置从上方或左边过不来，也去不了下方或右边，`dp[i][j] = 0`

机器人每次只能向下或者向右移动一步，表明**当前位置可能从上方或者左边走来的**

- 当前位置只能从「左边」走来，即第一行，`dp[i][j] = dp[i][j-1]`
- 当前位置只能从「上方」走来，即第一列，`dp[i][j] = dp[i-1][j]`
- 当前位置「即能从上方又能从左边」走来，`dp[i][j] = dp[i][j-1] + dp[i-1][j]`

**3. 初始化**

`dp[0][0] = 1`  起点为 1

**4. 输出**

`dp[m-1][n-1] `

**空间优化**

不优化

**复杂度分析**

时间复杂度：`O(m * n)`

空间复杂度：`O(m * n)`

```c++
class Solution {
public:
    int uniquePathsWithObstacles(vector<vector<int>>& obstacleGrid) {
        if (obstacleGrid[0][0] == 1) return 0;

        int rows = obstacleGrid.size();
        int cols = obstacleGrid[0].size();
        vector<vector<int>> dp(rows, vector<int>(cols, 0));
        dp[0][0] = 1;

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (obstacleGrid[r][c] == 1) {
                    dp[r][c] == 0;
                    continue;
                }
                if (r == 0 && c > 0) {  // 第一行
                    dp[r][c] = dp[r][c - 1];
                } else if (r > 0 && c == 0) {  // 第一列
                    dp[r][c] = dp[r - 1][c];
                } else if (r > 0 && c > 0) {
                    dp[r][c] = dp[r][c - 1] + dp[r - 1][c];
                }
            }
        }

        return dp[rows - 1][cols - 1];
    }
};
```

### [64. 最小路径和](https://leetcode-cn.com/problems/minimum-path-sum/)

给定一个包含非负整数的 `m * n` 网格 `grid` ，请找出一条从左上角到右下角的路径，使得路径上的数字总和为最小。

**说明：**每次只能向下或者向右移动一步。

![64](/Users/zhangdong/Desktop/algo/Algorithm/3-动态规划/doc/64.jpeg)

```
输入：grid = [[1,3,1],[1,5,1],[4,2,1]]
输出：7
解释：因为路径 1→3→1→1→1 的总和最小。

输入：grid = [[1,2,3],[4,5,6]]
输出：12
```

**1. 定义状态**

`dp[r][c]` 为到达位置 `(r,c)` 的最小累加和

**2. 状态转移方程**

机器人每次只能向下或者向右移动一步，表明**当前位置可能从上方或者左边走来的**

- 当前位置只能从「左边」走来，即第一行，`dp[r][c] = dp[r][c-1] + grid[r][c]`
- 当前位置只能从「上方」走来，即第一列，`dp[r][c] = dp[r-1][c] + grid[r][c]`
- 当前位置「即能从上方又能从左边」走来，那选「累加和最小的方向」，`dp[r][c] = min(dp[r][c-1], dp[r-1][c]) + grid[r][c]`

**3. 初始化**

`dp[0][0] = 1`  起点为 1

**4. 输出**

`dp[rows-1][cols-1] `

**空间优化**

不优化

**复杂度分析**

时间复杂度：`O(m * n)`

空间复杂度：`O(m * n)`

```c++
class Solution {
public:
    int minPathSum(vector<vector<int>>& grid) {
        int rows = grid.size();
        int cols = grid[0].size();

        vector<vector<int>> dp(rows, vector<int>(cols, 0));
        dp[0][0] = grid[0][0];

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (r == 0 && c > 0) {  // 第一行
                    dp[r][c] = dp[r][c - 1] + grid[r][c];
                } else if (r > 0 && c == 0) {  // 第一列
                    dp[r][c] = dp[r - 1][c] + grid[r][c];
                } else if (r > 0 && c > 0) {
                    dp[r][c] = min(dp[r][c - 1], dp[r - 1][c]) + grid[r][c];
                }
            }
        }
        return dp[rows - 1][cols - 1];
    }
};
```

#### 进阶一：输出总和最低的路径呢

从原问题我们知道，我们需要从 (0,0) 一步步转移到 (m-1,n-1)。

也就是我们需要扫描完整个方块（转移完所有的状态），才能得到答案。

那么显然，我们可以使用额外的数据结构来记录，我们是如何一步步转移到 f[m-1][n-1] 的。

当整个 dp 过程结束后，我们再用辅助记录的数据结构来回推我们的路径。

同时，由于我们原有的 dp 部分已经创建了一个二维数组来存储状态值，这次用于记录「上一步」的 trace 数组我们改用一维数组来记录。

【重要】`vector<int> trace(rows * cols, 0)`  trace[当前下标] = 前一位下标

从终点 [rows-1, cols-1] 向前找到 [0, 0] 为止

```c++
class Solution {
public:
    int rows;
    int cols;

    int getIdx(int r, int c) { return r * cols + c; }

    vector<int> parseIdx(int idx) {
        int r = idx / cols;
        int c = idx % cols;
        return {r, c};
    }

    int minPathSum(vector<vector<int>>& grid) {
        rows = grid.size();
        cols = grid[0].size();

        vector<int> trace(rows * cols, 0);  // trace[当前下标] = 前一位下标

        vector<vector<int>> dp(rows, vector<int>(cols, 0));
        dp[0][0] = grid[0][0];

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (r == 0 && c > 0) {  // 第一行
                    dp[r][c] = dp[r][c - 1] + grid[r][c];
                    trace[getIdx(r, c)] = getIdx(r, c - 1);
                } else if (r > 0 && c == 0) {  // 第一列
                    dp[r][c] = dp[r - 1][c] + grid[r][c];
                    trace[getIdx(r, c)] = getIdx(r - 1, c);
                } else if (r > 0 && c > 0) {
                    if (dp[r][c - 1] < dp[r - 1][c]) {
                        dp[r][c] = dp[r][c - 1] + grid[r][c];
                        trace[getIdx(r, c)] = getIdx(r, c - 1);
                    } else {
                        dp[r][c] = dp[r - 1][c] + grid[r][c];
                        trace[getIdx(r, c)] = getIdx(r - 1, c);
                    }
                }
            }
        }

        // 从「结尾」开始，逆序往前找「上一步」
        int cur = getIdx(rows - 1, cols - 1);
        string path =
            "(" + to_string(rows - 1) + "," + to_string(cols - 1) + ")";
        while (cur != 0) {
            cur = trace[cur];
            vector<int> tmp = parseIdx(cur);
            int r = tmp[0];
            int c = tmp[1];
            path = "(" + to_string(r) + "," + to_string(c) + ")" + "->" + path;
        }
        cout << path << endl;

        return dp[rows - 1][cols - 1];
    }
};
```

#### 进阶二：如果方块中存在负权，如何求解

如果考虑方块中增加负权的话，自然还需要增加一个限制：每个格子只能访问一次，否则会存在无数次访问负权格子的路径。

这时候问题就转换为「图论」问题，变成一个「最小生成树」问题了。

将每个格子 **往右** 和 **往下** 两个方向看做两条无向边，使用 **Prim算法/Kruskal算法** 求解。

这部分我们在之后的图论再讲。

**不解，感觉存在负权也可以算出路径**







剩余未做题目：

| 题目                                                         | 题解                                                         | 难度 | 推荐指数 |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- | -------- |
| [10. 正则表达式匹配](https://leetcode-cn.com/problems/regular-expression-matching) | [LeetCode 题解链接](https://leetcode-cn.com/problems/regular-expression-matching/solution/shua-chuan-lc-dong-tai-gui-hua-jie-fa-by-zn9w/) | 困难 | 🤩🤩🤩🤩     |
| [44. 通配符匹配](https://leetcode-cn.com/problems/wildcard-matching/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/wildcard-matching/solution/gong-shui-san-xie-xiang-jie-dong-tai-gui-ifyx/) | 困难 | 🤩🤩🤩🤩     |
| [1751. 最多可以参加的会议数目 II](https://leetcode-cn.com/problems/maximum-number-of-events-that-can-be-attended-ii/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/maximum-number-of-events-that-can-be-attended-ii/solution/po-su-dp-er-fen-dp-jie-fa-by-ac_oier-88du/) | 困难 | 🤩🤩🤩      |
| [1787. 使所有区间的异或结果为零](https://leetcode-cn.com/problems/make-the-xor-of-all-segments-equal-to-zero/) | [LeetCode 题解链接](https://leetcode-cn.com/problems/make-the-xor-of-all-segments-equal-to-zero/solution/gong-shui-san-xie-chou-xiang-cheng-er-we-ww79/) | 困难 | 🤩🤩🤩🤩     |

