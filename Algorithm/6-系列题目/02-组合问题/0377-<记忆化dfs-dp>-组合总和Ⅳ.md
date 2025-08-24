题目：[377. 组合总和 Ⅳ](https://leetcode.cn/problems/combination-sum-iv/)

题解：https://leetcode.cn/problems/combination-sum-iv/solution/fu-xue-ming-zhu-cong-ji-yi-hua-di-gui-tu-rqwy/

给你一个由 **不同** 整数组成的数组 `nums` ，和一个目标整数 `target` 。请你从 `nums` 中找出并返回总和为 `target` 的元素组合的个数。

题目数据保证答案符合 32 位整数范围。

**示例 1：**

```
输入：nums = [1,2,3], target = 4
输出：7
解释：
所有可能的组合为：
(1, 1, 1, 1)
(1, 1, 2)
(1, 2, 1)
(1, 3)
(2, 1, 1)
(2, 2)
(3, 1)
请注意，顺序不同的序列被视作不同的组合。
```

**示例 2：**

```
输入：nums = [9], target = 3
输出：0
```

提示：

- 1 <= nums.length <= 200
- 1 <= nums[i] <= 1000
- nums 中的所有元素 互不相同
- 1 <= target <= 1000

## 方法一：递归

```cpp
class Solution {
public:
    vector<int> options;

    // 返回目标为 target 的方案数
    int dfs(int t) {
        if (t < 0) return 0;
        if (t == 0) return 1;
        if (vis.count(t)) return vis[t];
        for (int op : options) {
            res += dfs(t - op);
        }
        return res;
    }
    int combinationSum4(vector<int>& nums, int target) {
        options = nums;
        return dfs(target);
    }
};
```

同样的 target 会重复计算，因此时间复杂度很高，可以进行记忆化dfs

## 方法二：记忆化dfs

```cpp
class Solution {
public:
    vector<int> options;
    unordered_map<int, int> vis;

    // 返回目标为 target 的方案数
    int dfs(int t) {
        if (t < 0) return 0;
        if (t == 0) return 1;
        if (vis.count(t)) return vis[t];
        int res = 0;
        for (int op : options) {
            res += dfs(t - op);
        }
        vis[t] = res;
        return res;
    }
    int combinationSum4(vector<int>& nums, int target) {
        options = nums;
        return dfs(target);
    }
};
```

## 方法三：动态规划

理解了「记忆化递归」之后，写出动态规划只有一步之遥。**递归是自顶向下**的计算方式（大问题->小问题），而**动态规划是自底向上**的计算方式（小问题->大问题）。

动态规划也同样地定义 `dp` 数组，`dp[i]` 表示从 `nums` 中抽取元素组成 `target` 的方案数。

`dp` 数组的长度是 `target + 1`。其中 `dp[0]` 表示从数组中抽取任何元素组合成 `0` 的方案数，根据我们在递归时的分析，我们知道需要令 `dp[0] = 1`。其他位置的 `dp[i]` 需要初始化为 `0`，表示我们还没有计算过这个位置，默认的方案数为 `0`。

想要计算得到 `target`，需要把 `dp[1~target]` 的各个元素都计算出来。每个位置的计算都是为了后面的计算做准备。

动态规划的代码如下，是从记忆化递归改造而来。

```cpp
#define ULL unsigned long long

class Solution {
public:
    int combinationSum4(vector<int>& nums, int target) {
        ULL dp[1001];
        memset(dp, 0, sizeof(ULL) * 1001);

        dp[0] = 1;
        for (int t = 1; t <= target; t++) {
            for (int num : nums) {
                if (t >= num) dp[t] += dp[t - num];
            }
        }

        return dp[target];
    }
};
```

