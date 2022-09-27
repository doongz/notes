题目：[剑指 Offer 39. 数组中出现次数超过一半的数字](https://leetcode.cn/problems/shu-zu-zhong-chu-xian-ci-shu-chao-guo-yi-ban-de-shu-zi-lcof/)

因为题目中已知存在一个超过一半个数的数字，因此不用判断最后剩下的那个数字是否是答案

```c++
class Solution {
public:
    int majorityElement(vector<int>& nums) {
        int x = 0;
        int votes = 0;
        for (int num : nums) {
            if (votes == 0) {
                x = num;
                votes = 1;
            } else {
                if (x == num) {
                    votes++;
                } else {
                    votes--;
                }
            }
        }
        return x;
    }
};
```

