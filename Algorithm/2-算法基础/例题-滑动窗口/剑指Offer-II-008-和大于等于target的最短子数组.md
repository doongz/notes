题目：[剑指 Offer II 008. 和大于等于 target 的最短子数组](https://leetcode.cn/problems/2VG8Kg/)

```c++
class Solution {
public:
    int minSubArrayLen(int target, vector<int>& nums) {
        int n = nums.size();
        int l = 0;
        int r = 0;
        int window = 0;
        int ans = INT_MAX;

        while (r < n) {
            window += nums[r];
            while (l <= r && window >= target) {  // l <= r 有等于是为了单个元素
                ans = min(ans, r - l + 1);
                window -= nums[l];
                l++;
            }
            r++;
        }
        return ans == INT_MAX ? 0 : ans;
    }
};
```

