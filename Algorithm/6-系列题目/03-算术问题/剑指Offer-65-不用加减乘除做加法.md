题目：[剑指 Offer 65. 不用加减乘除做加法](https://leetcode.cn/problems/bu-yong-jia-jian-cheng-chu-zuo-jia-fa-lcof/)

写一个函数，求两个整数之和，要求在函数体内不得使用 “+”、“-”、“*”、“/” 四则运算符号。

**示例:**

```
输入: a = 1, b = 1
输出: 2
```

**提示：**

- `a`, `b` 均可能是负数或 0
- 结果不会溢出 32 位整数

---

```c++
class Solution {
public:
    int add(int a, int b) {
        while(b != 0) { // 当进位为 0 时跳出
            int c = (unsigned int) (a & b) << 1;  // c = 进位
            a ^= b; // a = 非进位和
            b = c; // b = 进位
        }
        return a;
    }
};


class Solution {
public:
    int add(int a, int b) {
        if (b == 0) return a;
        return add(a ^ b, (unsigned int)(a & b) << 1);
    }
};
```

