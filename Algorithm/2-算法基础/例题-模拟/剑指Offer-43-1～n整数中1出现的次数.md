题目：[剑指 Offer 43. 1～n 整数中 1 出现的次数](https://leetcode.cn/problems/1nzheng-shu-zhong-1chu-xian-de-ci-shu-lcof/)

题解：[面试题43. 1～n 整数中 1 出现的次数（清晰图解）](https://leetcode.cn/problems/1nzheng-shu-zhong-1chu-xian-de-ci-shu-lcof/solution/mian-shi-ti-43-1n-zheng-shu-zhong-1-chu-xian-de-2/)

```c++
class Solution {
public:
    int countDigitOne(int n) {
        int high = n / 10;
        int low = 0;
        int cur = n % 10;
        long long digit = 1;
        int ans = 0;

        while (high != 0 || cur != 0) {
            if (cur == 0) {
                ans += high * digit;
            } else if (cur == 1) {
                ans += high * digit + low + 1;
            } else {
                ans += (high + 1) * digit;
            }
            low += cur * digit;
            cur = high % 10;
            high /= 10;
            digit *= 10;
        }
        return ans;
    }
};
```