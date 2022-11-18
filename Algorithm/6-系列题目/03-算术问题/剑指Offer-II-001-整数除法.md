题目：[剑指 Offer II 001. 整数除法](https://leetcode.cn/problems/xoh6Oh/)

题解：[简单易懂Java/C++ /Python/js/go - 整数除法(剑指)](https://leetcode.cn/problems/xoh6Oh/solution/jian-dan-yi-dong-javac-pythonjs-zheng-sh-e8r6/)

给定两个整数 `a` 和 `b` ，求它们的除法的商 `a/b` ，要求不得使用乘号 `'*'`、除号 `'/'` 以及求余符号 `'%'` 。

注意:

- 整数除法的结果应当截去（`truncate`）其小数部分，例如：`truncate(8.345) = 8` 以及 `truncate(-2.7335) = -2`
- 假设我们的环境只能存储 32 位有符号整数，其数值范围是 `[−231, 231−1]`。本题中，如果除法结果溢出，则返回 `231 − 1`

```
示例 1：

输入：a = 15, b = 2
输出：7
解释：15/2 = truncate(7.5) = 7

示例 2：

输入：a = 7, b = -3
输出：-2
解释：7/-3 = truncate(-2.33333..) = -2

示例 3：

输入：a = 0, b = 1
输出：0

示例 4：

输入：a = 1, b = 1
输出：1
```

**提示:**

- `-231 <= a, b <= 231 - 1`
- `b != 0`

注意：本题与主站 29 题相同：https://leetcode-cn.com/problems/divide-two-integers/



```c++
class Solution {
public:
    int divide(int a, int b) {
        if (a == INT_MIN && b == -1) return INT_MAX;

        int res = 0;
        // 处理边界，防止转正数溢出
        // 除数绝对值最大，结果必为 0 或 1
        if (b == INT_MIN) {
            return a == b ? 1 : 0;
        }

        // 被除数先减去一个除数
        if (a == INT_MIN) {
            a -= -abs(b);
            res += 1;
        }

        int sign = (a > 0) ^ (b > 0) ? -1 : 1;

        int ua = abs(a);
        int ub = abs(b);
        for (int i = 31; i >= 0; i--) {
            if ((ua >> i) >= ub) {
                ua = ua - (ub << i);
                // 代码优化：这里控制 ans 大于等于 INT_MAX
                if (res > INT_MAX - (1 << i)) {
                    return INT_MIN;
                }
                res += 1 << i;
            }
        }
        // bug 修复：因为不能使用乘号，所以将乘号换成三目运算符
        return sign == 1 ? res : -res;
    }
};
```

