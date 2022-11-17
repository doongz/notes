题目：[剑指 Offer 46. 把数字翻译成字符串](https://leetcode.cn/problems/ba-shu-zi-fan-yi-cheng-zi-fu-chuan-lcof/)

给定一个数字，我们按照如下规则把它翻译为字符串：0 翻译成 “a” ，1 翻译成 “b”，……，11 翻译成 “l”，……，25 翻译成 “z”。一个数字可能有多个翻译。请编程实现一个函数，用来计算一个数字有多少种不同的翻译方法。

示例 1:

```
输入: 12258
输出: 5
解释: 12258有5种不同的翻译，分别是"bccfi", "bwfi", "bczi", "mcfi"和"mzi"
```

---

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

