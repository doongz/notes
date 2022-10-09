题目：[剑指 Offer II 009. 乘积小于 K 的子数组](https://leetcode.cn/problems/ZVAVXX/)

固定右窗口，进行统计

统计以 nums[i] 为结尾（固定右端点）的合法子数组个数（左端点个数）为 i−j+1

```c++
class Solution {
public:
    int numSubarrayProductLessThanK(vector<int>& nums, int k) {
        if (k <= 1) return 0;  // 特殊处理
        int n = nums.size();
        int l = 0;
        int r = 0;
        int window = 1;
        int ans = 0;

        while (r < n) {
            window *= nums[r];
            while (l < r && window >= k) {
                window /= nums[l];
                l++;
            }
            // 此时窗口内刚好满足 window < k
            // 统计以 nums[i] 为结尾（固定右端点）的合法子数组个数（左端点个数）为 i−j+1
            ans += r - l + 1;
            r++;
        }

        return ans;
    }
};
```

