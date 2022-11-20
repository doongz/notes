题目：[51. N 皇后](https://leetcode.cn/problems/n-queens/)

按照国际象棋的规则，皇后可以攻击与之处在同一行或同一列或同一斜线上的棋子。

**n 皇后问题** 研究的是如何将 `n` 个皇后放置在 `n×n` 的棋盘上，并且使皇后彼此之间不能相互攻击。

给你一个整数 `n` ，返回所有不同的 **n 皇后问题** 的解决方案。

每一种解法包含一个不同的 **n 皇后问题** 的棋子放置方案，该方案中 `'Q'` 和 `'.'` 分别代表了皇后和空位。

**示例 1：**

![img](https://assets.leetcode.com/uploads/2020/11/13/queens.jpg)

```
输入：n = 4
输出：[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
解释：如上图所示，4 皇后问题存在两个不同的解法。
```

**示例 2：**

```
输入：n = 1
输出：[["Q"]]
```

**提示：**

- `1 <= n <= 9`

## 题解：回溯

一层一层做决策，选下一层的时候做有效性判断

- 由于是一层一层做决策，同层不会同时存在
- 同一列上不能有
- 左上到右下的主对角线不能有
- 右上到左下的副对角线不能有

关键点在于，两条斜线怎样判断

![image.png](https://pic.leetcode-cn.com/1599142979-VEuEDb-image.png)

这两个 vis 的个数 = 行 + 列 - 1

主对角线因为有负数，(横坐标-纵坐标)后的值要有偏移，偏移量为 n-1，vis 中的下标为 (row - col) + n - 1

副对角线的vis下标为 row + col，直接可以用

```c++
class Solution {
private:
    int n;
    vector<bool> vis_col;
    vector<bool> vis_zhu;
    vector<bool> vis_fu;
    vector<vector<string>> ans;

    vector<string> gen_path() {
        string sub = "";
        vector<string> path;
        for (int i = 0; i < n; i++) {
            sub += '.';
        }
        for (int i = 0; i < n; i++) {
            path.push_back(sub);
        }
        return path;
    }

    // 要考察的行
    void dfs(int r, vector<string> &path) {
        if (r == n) {
            ans.push_back(path);
            return;
        }
        for (int c = 0; c < n; c++) {
            if (vis_col[c]) continue;              // 同列不能有
            if (vis_zhu[r - c + n - 1]) continue;  // 同主对角线不能有
            if (vis_fu[r + c]) continue;           // 同副对角线不能有

            vis_col[c] = true;
            vis_zhu[r - c + n - 1] = true;
            vis_fu[r + c] = true;
            path[r][c] = 'Q';

            dfs(r + 1, path);

            path[r][c] = '.';
            vis_col[c] = false;
            vis_zhu[r - c + n - 1] = false;
            vis_fu[r + c] = false;
        }
    }

public:
    vector<vector<string>> solveNQueens(int _n) {
        n = _n;
        vis_col.resize(n, false);
        vis_zhu.resize(n + n - 1, false);
        vis_fu.resize(n + n - 1, false);
        vector<string> path = gen_path();

        dfs(0, path);
        return ans;
    }
};
```

