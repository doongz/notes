题目：[剑指 Offer II 010. 和为 k 的子数组](https://leetcode.cn/problems/QTMn0o/)

题解见 560 题

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

