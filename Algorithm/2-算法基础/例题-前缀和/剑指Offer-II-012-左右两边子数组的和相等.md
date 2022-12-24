题目：[剑指 Offer II 012. 左右两边子数组的和相等](https://leetcode.cn/problems/tvdfij/)

给你一个整数数组 `nums` ，请计算数组的 **中心下标** 。

数组 **中心下标** 是数组的一个下标，其左侧所有元素相加的和等于右侧所有元素相加的和。

如果中心下标位于数组最左端，那么左侧数之和视为 `0` ，因为在下标的左侧不存在元素。这一点对于中心下标位于数组最右端同样适用。

如果数组有多个中心下标，应该返回 **最靠近左边** 的那一个。如果数组不存在中心下标，返回 `-1` 。

```
示例 1：

输入：nums = [1,7,3,6,5,6]
输出：3
解释：
中心下标是 3 。
左侧数之和 sum = nums[0] + nums[1] + nums[2] = 1 + 7 + 3 = 11 ，
右侧数之和 sum = nums[4] + nums[5] = 5 + 6 = 11 ，二者相等。

示例 2：

输入：nums = [1, 2, 3]
输出：-1
解释：
数组中不存在满足此条件的中心下标。

示例 3：

输入：nums = [2, 1, -1]
输出：0
解释：
中心下标是 0 。
左侧数之和 sum = 0 ，（下标 0 左侧不存在元素），
右侧数之和 sum = nums[1] + nums[2] = 1 + -1 = 0 。
```

**提示：**

- `1 <= nums.length <= 104`
- `-1000 <= nums[i] <= 1000` 

注意：本题与主站 724 题相同： https://leetcode-cn.com/problems/find-pivot-index/

```cpp
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

