题目：[剑指 Offer II 012. 左右两边子数组的和相等](https://leetcode.cn/problems/tvdfij/)

```c++
class Solution {
public:
    int pivotIndex(vector<int>& nums) {
        int n = nums.size();
        vector<int> pre_sum(n, 0);
        pre_sum[0] = nums[0];
        for (int i = 1; i < n; i++) {
            pre_sum[i] = pre_sum[i - 1] + nums[i];
        }

        for (int i = 0; i < n; i++) {
            if (i == 0) {
                if (pre_sum[n - 1] - pre_sum[0] == 0) return 0;
            } else if (i == n - 1) {
                if (pre_sum[n - 2] == 0) return n - 1;
            } else {
                if (pre_sum[i - 1] == pre_sum[n - 1] - pre_sum[i]) return i;
            }
        }

        return -1;
    }
};
```

