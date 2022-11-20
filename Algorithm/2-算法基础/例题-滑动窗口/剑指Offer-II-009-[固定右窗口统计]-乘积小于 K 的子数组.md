题目：[剑指 Offer II 009. 乘积小于 K 的子数组](https://leetcode.cn/problems/ZVAVXX/)

给定一个正整数数组 `nums`和整数 `k` ，请找出该数组内乘积小于 `k` 的连续的子数组的个数。

```
示例 1:

输入: nums = [10,5,2,6], k = 100
输出: 8
解释: 8 个乘积小于 100 的子数组分别为: [10], [5], [2], [6], [10,5], [5,2], [2,6], [5,2,6]。
需要注意的是 [10,5,2] 并不是乘积小于100的子数组。

示例 2:

输入: nums = [1,2,3], k = 0
输出: 0
```

**提示:** 

- `1 <= nums.length <= 3 * 104`
- `1 <= nums[i] <= 1000`
- `0 <= k <= 106`

---

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

