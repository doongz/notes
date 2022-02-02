#### [523. 连续的子数组和](https://leetcode-cn.com/problems/continuous-subarray-sum/)

[题解](https://leetcode-cn.com/problems/continuous-subarray-sum/solution/gong-shui-san-xie-tuo-zhan-wei-qiu-fang-1juse/)

题目的数据量为 `1 <= nums.length <= 10^5`，简单使用前缀和优化的做法 (O(n^2) 不能满足要求。

**需要从 k 的倍数作为切入点来做。**

预处理前缀和数组 sum，方便快速求得某一段区间的和。然后假定 [i, j] 是我们的目标区间，那么有：

$$
sum[j]-sum[i] = n*k
$$

变形：

$$
\frac{sum[j]}{k} - \frac{sum[i-1]}{k} = n
$$

**「同余性质」： b 和 a 模 k 相同，那么 b - a 为 k 的倍数**

将取余结果存入set，如果枚举某个右端点 j 时发现存在某个左端点 i 符合要求，则返回 `True`。

- 时间复杂度：`O(n)`
- 空间复杂度：`O(n)`

```python
class Solution:
    def checkSubarraySum(self, nums: List[int], k: int) -> bool:
        sz = len(nums)
        pre_sum = [0 for _ in range(sz+1)]
        for i in range(sz):
            pre_sum[i+1] = pre_sum[i] + nums[i]
        
        trace = set()
        for i in range(2, sz+1):
            trace.add(pre_sum[i-2] % k)
            if pre_sum[i] % k in trace:
                return True
        return False
```

**拓展**

一个数组，如果其中一段连续的子数组之和是k的倍数，这个区间就为k倍区间，数组中有几个k倍区间

```python
class Solution:
    def checkSubarraySum(self, nums: List[int], k: int) -> bool:
        sz = len(nums)
        pre_sum = [0 for _ in range(sz+1)]
        for i in range(sz):
            pre_sum[i+1] = pre_sum[i] + nums[i]
        
        trace = collections.defaultdict(int)
        cnt = 0
        for i in range(1, sz+1):
            yu = pre_sum[i] % k
            cnt += trace[yu]
            trace[yu] += 1
        return cnt
```

