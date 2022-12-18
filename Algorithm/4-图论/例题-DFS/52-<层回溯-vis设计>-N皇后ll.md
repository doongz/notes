题目：[52. N皇后 II](https://leetcode.cn/problems/n-queens-ii/)

**n 皇后问题** 研究的是如何将 `n` 个皇后放置在 `n × n` 的棋盘上，并且使皇后彼此之间不能相互攻击。

给你一个整数 `n` ，返回 **n 皇后问题** 不同的解决方案的数量。

**示例 1：**

![img](https://assets.leetcode.com/uploads/2020/11/13/queens.jpg)

```
输入：n = 4
输出：2
解释：如上图所示，4 皇后问题存在两个不同的解法。
```

**示例 2：**

```
输入：n = 1
输出：1
```

**提示：**

- `1 <= n <= 9`

---

把 N皇后 的path去掉即可

```c++
class Solution {
private:
    int n;
    vector<bool> vis_col;
    vector<bool> vis_zhu;
    vector<bool> vis_fu;
    int ans = 0;

    // 要考察的行
    void dfs(int r) {
        if (r == n) {
            ans++;
            return;
        }
        for (int c = 0; c < n; c++) {
            if (vis_col[c]) continue;              // 同列不能有
            if (vis_zhu[r - c + n - 1]) continue;  // 同主对角线不能有
            if (vis_fu[r + c]) continue;           // 同副对角线不能有

            vis_col[c] = true;
            vis_zhu[r - c + n - 1] = true;
            vis_fu[r + c] = true;

            dfs(r + 1);

            vis_col[c] = false;
            vis_zhu[r - c + n - 1] = false;
            vis_fu[r + c] = false;
        }
    }

public:
    int totalNQueens(int _n) {
        n = _n;
        vis_col.resize(n, false);
        vis_zhu.resize(n + n - 1, false);
        vis_fu.resize(n + n - 1, false);

        dfs(0);
        return ans;
    }
};
```

