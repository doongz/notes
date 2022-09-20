题目：[剑指 Offer 16. 数值的整数次方](https://leetcode.cn/problems/shu-zhi-de-zheng-shu-ci-fang-lcof/)

## 方法：快速幂

```c++
class Solution {
public:
    double myPow(double x, int n) {
        if (x == 0) return 0;
        long b = n;
        double res = 1.0;

        if (b < 0) {
            x = 1 / x;
            b = -b;
        }
        while (b > 0) {
            // 最后一位为1，需要乘上该位上的权重
            if ((b & 1) == 1) {
                res *= x;
            }
            x *= x;
            b >>= 1;
        }
        return res;
    }
};
```