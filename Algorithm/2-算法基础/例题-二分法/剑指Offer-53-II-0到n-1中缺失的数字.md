题目：[剑指 Offer 53 - II. 0～n-1中缺失的数字](https://leetcode.cn/problems/que-shi-de-shu-zi-lcof/)

一个长度为n-1的递增排序数组中的所有数字都是唯一的，并且每个数字都在范围0～n-1之内。在范围0～n-1内的n个数字中有且只有一个数字不在该数组中，请找出这个数字。

**示例 1:**

```
输入: [0,1,3]
输出: 2
```

**示例 2:**

```
输入: [0,1,2,3,4,5,6,7,9]
输出: 8
```

**限制：**

```
1 <= 数组长度 <= 10000
```

---

```c++
class Solution {
public:
    int missingNumber(vector<int>& nums) {
        int left = 0;
        int right = nums.size() - 1;
        while (left <= right) {
            int mid = left + ((right - left) >> 1);
            if (nums[mid] == mid) { // 左区间正确
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return left;
    }
};
```



```c++
class Solution {
public:
    int missingNumber(vector<int>& nums) {
        int n = nums.size();
        int pre = nums[0];
        for (int i = 1; i < n; i++) {
            if (nums[i] != pre + 1) {
                return pre + 1;
            }
            pre++;
        }
        if (nums[0] == 0) return *nums.rbegin() + 1;
        return nums[0] - 1;
    }
};
```

