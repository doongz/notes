[1818. 绝对差值和](https://leetcode-cn.com/problems/minimum-absolute-sum-difference/)

## 方法：排序+二分

我们在进行处理前，**先对 nums1 进行「拷贝排序」**，因为 nums1 和 nums2 的位置是相对应的

然后 在遍历 nums1 和 nums2 计算总的差值 sum 时，**通过对排过序的 nums1 进行二分查找，找到「最合适」替换 nums[i] 的值**

具体的，当我们处理到第 i 位时，假设该位的原差值为 x = abs(nums1[i] - nums2[i])，然后从 nums1 中通过二分找到最接近 nums2[i] 的值，计算一个新的差值 nd（注意要检查分割点与分割点的下一位），如果满足 nd < x 说明存在一个替换方案使得差值变小，我们使用变量 maxn 记下来这个替换方案所带来的变化（后半截差的），并不断更新 maxn。

> 总差的(diff) - 前半截差的 = 后半截差的

当整个数组被处理完，maxn 存储着后半截差的最大的，此时 sum - maxn 即是其余值的 diff和 + 前半截差的最小的，就是答案

```c++
const int mod = 1e9 + 7;

class Solution {
public:
    int minAbsoluteSumDiff(vector<int>& nums1, vector<int>& nums2) {
        int n = nums1.size();
        vector<int> nums1_copy(nums1);
        sort(nums1_copy.begin(), nums1_copy.end());
        long long sum = 0;
        int maxn = 0;
        for (int i = 0; i < n; i++) {
            int val1 = nums1[i];  // 注意这里使用原数组 nums1 中取值
            int val2 = nums2[i];
            int diff = abs(val1 - val2);
            sum += diff;

            int idx = lower_bound(nums1_copy.begin(), nums1_copy.end(), val2) - nums1_copy.begin();
            if (idx < n) {
                maxn = max(maxn, diff - (nums1_copy[idx] - val2));
            }
            if (idx > 0) {
                maxn = max(maxn, diff - (val2 - nums1_copy[idx - 1]));
            }
        }
        return (sum - maxn) % mod;
    }
};
```

