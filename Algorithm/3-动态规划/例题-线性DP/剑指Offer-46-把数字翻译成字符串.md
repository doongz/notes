题目：[剑指 Offer 46. 把数字翻译成字符串](https://leetcode.cn/problems/ba-shu-zi-fan-yi-cheng-zi-fu-chuan-lcof/)

```c++
class Solution:
    def translateNum(self, num: int) -> int:
        nums =[int(i) for i in str(num)]
        n = len(nums)

        # dp[i+1] 表示以 nums[i] 结尾的方法数量
        dp = [0 for _ in range(n + 1)]
        dp[0] = 1
        dp[1] = 1
        for i in range(1, n):
            double = nums[i-1] * 10 + nums[i]
            if double < 10 or double > 25: # 注意 07 08 09 这些也是无法转移的
                dp[i+1] = dp[i]
            else:
                dp[i+1] = dp[i] + dp[i-1]

        # print(dp)
        return dp[-1]
```

