题目：[剑指 Offer 65. 不用加减乘除做加法](https://leetcode.cn/problems/bu-yong-jia-jian-cheng-chu-zuo-jia-fa-lcof/)



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

