题目：[剑指 Offer II 011. 0 和 1 个数相同的子数组](https://leetcode.cn/problems/A1NYOS/description/)

给定一个二进制数组 `nums` , 找到含有相同数量的 `0` 和 `1` 的最长连续子数组，并返回该子数组的长度。

```
示例 1：

输入: nums = [0,1]
输出: 2
说明: [0, 1] 是具有相同数量 0 和 1 的最长连续子数组。

示例 2：

输入: nums = [0,1,0]
输出: 2
说明: [0, 1] (或 [1, 0]) 是具有相同数量 0 和 1 的最长连续子数组。
```

**提示：**

- `1 <= nums.length <= 105`
- `nums[i]` 不是 `0` 就是 `1`

注意：本题与主站 525 题相同： https://leetcode-cn.com/problems/contiguous-array/

---

根据题意，我们可以轻易发现如下性质：如果答案非 0，那么子数组长度必然为偶数，且长度至少为 2。

具体的，我们在预处理前缀和时，将 nums[i] 为 0 的值当做 −1 处理。

从而将问题转化为：如何求得最长一段区间和为 0 的子数组。 同时使用「哈希表」来记录「某个前缀和出现的最小下标」是多少。



```c++
class Solution {
public:
    int findMaxLength(vector<int>& nums) {
        int n = nums.size();
        vector<int> pre_sum(n + 1, 0);
        for (int i = 1; i <= n; i++) {
            if (nums[i - 1] == 0) {
                pre_sum[i] = -1 + pre_sum[i - 1];
            } else {
                pre_sum[i] = 1 + pre_sum[i - 1];
            }
        }
        int ans = 0;
        unordered_map<int, int> history;
        history[0] = 0;  // 记录左边界
        for (int i = 1; i <= n; i++) {
            if (history.count(pre_sum[i])) {
                // 如果在里面，将意味着子数组的和为0， 0 1的个数一样
                ans = max(ans, i - history[pre_sum[i]]);
            } else {
                // 不在里面，就记录，保证了最早出现的 pre_sum[i] 记录，以获得最长长度
                history[pre_sum[i]] = i;
            }
        }
        return ans;
    }
};
```



```c++
class Solution {
public:
    int findMaxLength(vector<int>& nums) {
        int n = nums.size();
        int pre_sum = 0;
        int ans = 0;
        unordered_map<int, int> history;
        history[0] = 0;

        for (int i = 1; i <= n; i++) {
            pre_sum += nums[i - 1] == 0 ? -1 : 1;
            if (history.count(pre_sum)) {
                ans = max(ans, i - history[pre_sum]);
            } else {
                history[pre_sum] = i;
            }
        }
        return ans;
    }
};
```

