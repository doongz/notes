题目：[132. 分割回文串 II](https://leetcode.cn/problems/palindrome-partitioning-ii/)

给你一个字符串 `s`，请你将 `s` 分割成一些子串，使每个子串都是回文。

返回符合要求的 **最少分割次数** 。

**示例 1：**

```
输入：s = "aab"
输出：1
解释：只需一次分割就可将 s 分割成 ["aa","b"] 这样两个回文子串。
```

**示例 2：**

```
输入：s = "a"
输出：0
```

**示例 3：**

```
输入：s = "ab"
输出：1
```

**提示：**

- `1 <= s.length <= 2000`
- `s` 仅由小写英文字母组成

---

## 动态规划

如果在 [131. 分割回文串](https://leetcode.cn/link/?target=https://mp.weixin.qq.com/s?__biz=MzU4NDE3MTEyMA==&mid=2247487047&idx=1&sn=117c48f20778868442fce44e100d2ea8&chksm=fd9ca558caeb2c4eb1bff4f0878ff796feabe523657c2aafea0b2d1c7026e1c0572ab1e6d205&token=635532356&lang=zh_CN#rd) 有使用到 DP 进行预处理的话。

这道题就很简单了，就是一道常规的动态规划题。

为了方便，我们约定所有下标从 1 开始。

即对于长度为 n 的字符串，我们使用 [1,n] 进行表示。

估计不少看过三叶题解的同学都知道，这样做的目的是为了减少边界情况判断，这本身也是对于「哨兵」思想的运用。

#### 递推「最小分割次数」思路

我们定义 f[r] 为将 [1,r] 这一段字符分割为若干回文串的最小分割次数，那么最终答案为 f[n]。

不失一般性的考虑 f[r] 如何转移：

1. 从「起点字符」到「第 r 个字符」能形成回文串。那么最小分割次数为 0，此时有 f[r] = 0；
2. 从「起点字符」到「第 r 个字符」不能形成回文串。此时我们需要枚举左端点 l，如果 [l,r] 这一段是回文串的话，那么有 f[r] = f[l - 1] + 1。

在 2 中满足回文要求的左端点位置 l 可能有很多个，我们在所有方案中取一个 min 即可。

#### 快速判断「任意一段子串是否回文」思路

剩下的问题是，我们如何快速判断连续一段 [l, r][*l*,*r*] 是否为回文串，做法和昨天的 [131. 分割回文串](https://leetcode.cn/link/?target=https://mp.weixin.qq.com/s?__biz=MzU4NDE3MTEyMA==&mid=2247487047&idx=1&sn=117c48f20778868442fce44e100d2ea8&chksm=fd9ca558caeb2c4eb1bff4f0878ff796feabe523657c2aafea0b2d1c7026e1c0572ab1e6d205&token=635532356&lang=zh_CN#rd) 一模一样。

> PS. 在 [131. 分割回文串](https://leetcode.cn/link/?target=https://mp.weixin.qq.com/s?__biz=MzU4NDE3MTEyMA==&mid=2247487047&idx=1&sn=117c48f20778868442fce44e100d2ea8&chksm=fd9ca558caeb2c4eb1bff4f0878ff796feabe523657c2aafea0b2d1c7026e1c0572ab1e6d205&token=635532356&lang=zh_CN#rd)，数据范围只有 16，因此我们可以不使用 DP 进行预处理，而是使用双指针来判断是否回文也能过。但是该题数据范围为 2000（数量级为 10^3），使用朴素做法判断是否回文的话，复杂度会去到 O(n^3)（计算量为 10^9），必然超时。

因此我们不可能每次都使用双指针去线性扫描一遍 [l, r] 判断是否回文。

一个合理的做法是，我们先预处理出所有的 `g[l][r]`，`g[l][r]` 代表 [l,r] 这一段是否为回文串。

预处理 `g[l][r]` 的过程可以用递推去做。

要想 `g[l][r] = true` ，必须满足以下两个条件：

- `g[l+1][r−1]=true`
- `s[l] = s[r]`

由于状态 `g[l][r]` 依赖于状态 `g[l + 1][r - 1]`，因此需要我们左端点 l 是「从大到小」进行遍历；而右端点 r 是「从小到大」进行遍历。

因此最终的遍历过程可以整理为：右端点 r 一直往右移动（从小到大），在 r 固定情况下，左端点 l 在 r 在左边开始，一直往左移动（从大到小）。

时间复杂度：O(n*n)

```c++
class Solution {
public:
    int minCut(string s) {
        int n = s.size();

        // g[l][r] 代表 [l,r] 这一段是否为回文串
        vector<vector<bool>> g(n+1, vector<bool>(n+1));
        for (int r = 1; r <= n; r++) {
            for (int l = r; l >= 1; l--) {
                // 如果只有一个字符，则[l,r]属于回文
                if (l == r) {
                    g[l][r] = true;
                } else {
                    // 在 l 和 r 字符相同的前提下
                    if (s[l-1] == s[r-1]) {
                        // 如果 l 和 r 长度只有 2；或者 [l+1,r-1] 这一段满足回文，则[l,r]属于回文
                        if (r - l == 1 || g[l+1][r-1]) {
                            g[l][r] = true;
                        }
                    }
                }
            }
        }

        // f[r] 代表将 [1,r] 这一段分割成若干回文子串所需要的最小分割次数
        vector<int> f(n+1);
        for (int r = 1; r <= n; r++) {
            // 如果 [1,r] 满足回文，不需要分割
            if (g[1][r]) {
                f[r] = 0;
            } else {
                // 先设定一个最大分割次数（r 个字符最多消耗 r - 1 次分割）
                f[r] = r - 1;
                // 在所有符合 [l,r] 回文的方案中取最小值
                for (int l = 1; l <= r; l++) {
                    if (g[l][r]) f[r] = min(f[r], f[l - 1] + 1);
                }   
            }
        }
        return f[n];
    }
};
```

