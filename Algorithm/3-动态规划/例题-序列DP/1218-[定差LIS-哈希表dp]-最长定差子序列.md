题目：[1218. 最长定差子序列](https://leetcode-cn.com/problems/longest-arithmetic-subsequence-of-given-difference/)

## 方法：LIS 思想

**1. 状态定义**：

dp[nums[i]] 表示以 nums[i] 结尾的最长等差子序列的长度

**2. 状态转移方程**：

检查 nums[i] 的时候，在 [0, i-1] 的范围内寻找 pre = nums[i] - diff

- 如果找到了，dp[nums[i]] = dp[pre] + 1
- 没找到，dp[nums[i]] = 1

```
arr = [1,5,7,8,5,3,4,2,1], difference = -2
当遍历到 3 的时候，前面有两个 5，应该使用哪个 5 呢？
应该使用 idx=4 的那个5，因为 dp[4]=2，这个5的长度更长
```

这就引导我们「哈希表」来构造状态数组 dp {key : val}，val 为末尾数字为 key 的最长子序列的长度

以 O(1) 的时间复杂度找到前面那个数

**3. 初始化**：

dp 哈希表为空

**4. 返回**：

dp 数组中的最大值

**复杂度分析**：

时间复杂度：`O(n)`

空间复杂度：`O(n)`

下面的写法略显繁琐，但是非常明了，防止当 pre 不在 dp.keys() 中时，插入一条 dp[pre] = 0 的脏数据

```c++
class Solution {
public:
    int longestSubsequence(vector<int>& arr, int difference) {
        int n = arr.size();
        unordered_map<int, int> dp;

        dp[arr[0]] = 1;
        for (int i = 1; i < n; i++) {
            int pre = arr[i] - difference;
            if (dp.count(pre)) {
                dp[arr[i]] = dp[pre] + 1;
            } else {
                dp[arr[i]] = 1;
            }
        }
        int ans = 0;
        for (auto it = dp.begin(); it != dp.end(); it++) {
            ans = max(ans, it->second);
        }

        return ans;
    }
};
```

