题目：[剑指 Offer 15. 二进制中1的个数](https://leetcode.cn/problems/er-jin-zhi-zhong-1de-ge-shu-lcof/)

时间复杂度：`O(logn)`

```c++
class Solution {
public:
    int hammingWeight(uint32_t n) {
        // cout << n << endl;
        if (n == 0 || n == 1) {
            return n;
        }
        int cnt = 0;
        while (n != 0) {
            cnt++;
            n = n & (n - 1);
        }
        return cnt;
        
    }
};
```

