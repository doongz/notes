[1. 两数之和](https://leetcode-cn.com/problems/two-sum/)

## 方法一：记忆化map

使用哈希表，记录已经遍历过的值。如果剩余的值（target-cur）出现过，那就是答案

时间复杂度：`O(n)`

空间复杂度：`O(n)`

```c++
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        int n = nums.size();
        unordered_map<int, int> mem;
        for (int i = 0; i < n; i++) {
            if (mem.count(target - nums[i]) == 1){
                return {i, mem[target - nums[i]]};
            }
            mem[nums[i]] = i;
        }
        return {};
    }
};
```



