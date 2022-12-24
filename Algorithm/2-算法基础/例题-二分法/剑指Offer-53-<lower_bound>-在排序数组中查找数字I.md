[剑指 Offer 53 - I. 在排序数组中查找数字 I](https://leetcode-cn.com/problems/zai-pai-xu-shu-zu-zhong-cha-zhao-shu-zi-lcof/)

统计一个数字在排序数组中出现的次数。

```
示例 1:

输入: nums = [5,7,7,8,8,10], target = 8
输出: 2

示例 2:

输入: nums = [5,7,7,8,8,10], target = 6
输出: 0
```

提示：

0 <= nums.length <= 105
-109 <= nums[i] <= 109
nums 是一个非递减数组
-109 <= target <= 109

---

注意 lower_bound 的理解

```cpp
class Solution {
public:
    int search(vector<int>& nums, int target) {
        if (nums.empty()) {
            return 0;
        }
        int n = nums.size();
        int left = lower_bound(nums.begin(), nums.end(), target) - nums.begin();
        // cout << left << endl;
        // target 找不到，注意if内的顺序，防止越界
        if (left == n || nums[left] != target) {
            return 0;
        }
        int right = upper_bound(nums.begin(), nums.end(), target) - nums.begin();
        return right - left;
    }
};
```