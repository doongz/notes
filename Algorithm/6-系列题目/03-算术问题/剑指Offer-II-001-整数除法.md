题目：[剑指 Offer II 001. 整数除法](https://leetcode.cn/problems/xoh6Oh/)

题解：[简单易懂Java/C++ /Python/js/go - 整数除法(剑指)](https://leetcode.cn/problems/xoh6Oh/solution/jian-dan-yi-dong-javac-pythonjs-zheng-sh-e8r6/)

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

