题目：[剑指 Offer II 010. 和为 k 的子数组](https://leetcode.cn/problems/QTMn0o/)

给定一个整数数组和一个整数 `k` **，**请找到该数组中和为 `k` 的连续子数组的个数。

```
示例 1：

输入:nums = [1,1,1], k = 2
输出: 2
解释: 此题 [1,1] 与 [1,1] 为两种不同的情况

示例 2：

输入:nums = [1,2,3], k = 3
输出: 2
```

**提示:**

- `1 <= nums.length <= 2 * 104`
- `-1000 <= nums[i] <= 1000`
- `-107 <= k <= 107`

题解见 560 题

注意：本题与主站 560 题相同： https://leetcode-cn.com/problems/subarray-sum-equals-k/

```c++
class Solution {
public:
    int subarraySum(vector<int>& nums, int k) {
        int n = nums.size();
        unordered_map<int, int> history;
        history[0] = 1;
        int pre_sum = 0;
        int ans = 0;

        for (int i = 0; i < n; i++) {
            pre_sum += nums[i];
            if (history.count(pre_sum-k)) {
                ans += history[pre_sum-k];
            }
            history[pre_sum]++;
        }
        return ans;
    }
};
```

