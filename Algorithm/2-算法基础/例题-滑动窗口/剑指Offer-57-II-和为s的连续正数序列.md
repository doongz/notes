题目：[剑指 Offer 57 - II. 和为s的连续正数序列](https://leetcode.cn/problems/he-wei-sde-lian-xu-zheng-shu-xu-lie-lcof/)

```c++
class Solution {
public:
    vector<vector<int>> findContinuousSequence(int target) {
        int limit = (target & 1) ? target / 2 + 1 : target / 2;
        int left = 1;
        int right = 2;
        int window = 1;
        vector<vector<int>> ans;

        while (left < right && right <= limit) {
            window += right;

            while (left < right && window > target) {
                window -= left;
                left++;
            }

            if (window == target) {
                vector<int> res;
                for (int i = left; i <= right; i++) {
                    res.push_back(i);
                }
                ans.push_back(res);
            }

            right++;
        }

        return ans;
    }
};
```

