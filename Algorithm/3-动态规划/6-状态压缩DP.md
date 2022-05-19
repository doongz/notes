# 状态压缩 DP

**使用一个二进制数记录当前哪些数已被选，哪些数未被选，目的是为了可以使用位运算进行加速**

注意：num 不能太大，一般是 15 以下

```
我们可以通过一个具体的样例，来感受下「状态压缩」是什么意思：

例如一串二进制数 000...01010
代表值为 1 和值为 3 的数字已经被使用了，而值为 0、2 的节点尚未被使用。
```

然后再来看看使用「状态压缩」的话，一些基本的操作该如何进行：

假设变量 `state` 存放了「当前数的使用情况」

- 利用 `((state >> num) & 1) == 0` 判断 num 有没有用过，等于 0 没用过，大于 0 用过，`(1 << num) & state) == 0` 也行，但前者更好理解
- 利用 `(1 << num) | state` 记录 num 用过了
- `state & (~(1 << num))` 查看选择 num 之前的 state

## 一、位运算

```c++
#include <iostream>
#include <string>
#include <vector>

using namespace std;

string dec_to_bin(int dec) {
    vector<int> binL;
    while (dec != 0) {
        binL.push_back(dec % 2);
        dec = dec / 2;
    }
    // 结果是逆序的，需要反过来
    reverse(binL.begin(), binL.end());

    string bin;
    for (int b : binL) {
        bin += b + 48;
    }
    return bin;
}

int main() {
    int state = 0;  // 记录用过的数，初始时为0

    cout << ((1 << 3) & state) << endl;  // 0 检查 3 有没有被用过，没有
    state = (1 << 3) | state;            // 将 3 记录在 state 这个数中，传递下去
    cout << dec_to_bin(state) << endl;   // 1000

    cout << ((1 << 3) & state) << endl;  // 8 检查 3 有没有被用过，用过
    cout << ((1 << 4) & state) << endl;  // 0 检查 4 有没有被用过，没有
    state = (1 << 4) | state;            // 将 4 记录在 state 这个数中，传递下去
    cout << dec_to_bin(state) << endl;   // 11000

    cout << ((1 << 3) & state) << endl;  // 8 检查 3 有没有被用过，用过
    cout << ((1 << 4) & state) << endl;  // 16 检查 4 有没有被用过，用过
    cout << ((1 << 6) & state) << endl;  // 0 检查 6 有没有被用过，没有
    state = (1 << 6) | state;            // 将 6 记录在 state 这个数中，传递下去
    cout << dec_to_bin(state) << endl;   // 1011000

    int pre = state & (~(1 << 6));    // 查看选择 6 之前的 state
    cout << dec_to_bin(pre) << endl;  // 11000

    return 0;
}

```

## 二、例题

### [526. 优美的排列](https://leetcode.cn/problems/beautiful-arrangement/)

**1. 定义状态**

`dp[i][state]` 表示前 i 个数，且当前选择方案为状态 `state` 的方案个数

**这里的 status 代表或记录了前面 i 个数，哪些选了，哪些没选**

**2. 状态转移方程**

不失一般性的考虑 `dp[i][state]` 该如何转移，由于本题是求方案数，我们的转移方程必须做到「不重不漏」。

我们可以通过枚举当前位置 `i` 是选哪个数，假设位置 `i` 所选数值为 `k`，首先 `k` 值需要同时满足如下两个条件才能被选择：

- `state` 二进制中的第 `k` 位为 1；
- 要么 k 能被 i 整除，要么 i 能被 k 整除

那么根据状态定义，位置 i 选了数值 k，通过位运算我们可以直接得出决策位置 i 之前的状态是什么：`state & (~(1 << k))`

最终的 `dp[i][state]` 为当前位置 `i` 选择的是所有合法的 `k` 值的方案数之和：
$$
dp[i][state] = \sum^{n-1}_{k=0}dp[i-1][state \ \& \ \neg(1<<k)]
$$
由于给定的数值范围为 `[1,n]`，但实现上为了方便，我们使用 `state` 从右往左的第 0 位表示数值 1 选择情况，第 1 位表示数值 2 的选择情况 ... 即对选择数值 k 做一个 −1 的偏移

即，在对 state 使用 k-1 代表 k

**3. 初始化**

`d[0][0] = 1` 代表当我们不考虑任何数 `i=0` 的情况下，一个数都不选择（status = 0 二进制为 "00000"），为 1 种方案

**复杂度分析**

时间复杂度：共有 n * 2^n 的状态需要被转移，每次转移复杂度为 O(n)，整体复杂度为 O(n^2 * 2^n)

空间复杂度：O(n * 2^n)

```c++
class Solution {
public:
    int countArrangement(int n) {
        int mask = 1 << n;
        vector<vector<int>> dp(n + 1, vector<int>(mask, 0));
        dp[0][0] = 1;

        for (int i = 1; i <= n; i++) {
            // 枚举所有的状态
            for (int state = 0; state < mask; state++) {
                // 枚举位置 i（最后一位）选的数值是 k
                for (int k = 1; k <= n; k++) {
                    // 首先 k 在 state 中必须是 1，表示可以从前面的那个状态转移过来
                    if (((state >> (k-1)) & 1) == 0) continue;
                    // 数值 k 和位置 i 之间满足任一整除关系
                    if (k % i != 0 && i % k != 0) continue;
                    // state & (~(1 << (k - 1))) 代表将 state 中数值 k 的位置置零
                    dp[i][state] += dp[i - 1][state & (~(1 << (k - 1)))];
                }
            }
        }
        return dp[n][mask-1];
    }
};

```



