题目：[剑指 Offer 61. 扑克牌中的顺子](https://leetcode.cn/problems/bu-ke-pai-zhong-de-shun-zi-lcof/)

从**若干副扑克牌**中随机抽 `5` 张牌，判断是不是一个顺子，即这5张牌是不是连续的。2～10为数字本身，A为1，J为11，Q为12，K为13，而大、小王为 0 ，可以看成任意数字。A 不能视为 14。

**示例 1:**

```
输入: [1,2,3,4,5]
输出: True
```

**示例 2:**

```
输入: [0,0,1,2,5]
输出: True
```

**限制：**

数组长度为 5 

数组的数取值为 [0, 13] .



```python
class Solution:
    def isStraight(self, nums: List[int]) -> bool:
        nums.sort()
        cnt0 = 0
        flag = False # 是否找到第一个数

        for i in range(5):
            if nums[i] == 0:
                cnt0 += 1
            else: # 当前数不为 0
                if flag == False:
                    flag = True # 标记找到第一个数
                else:
                    if nums[i] == nums[i-1]: return False # 有相同的牌
                    diff = nums[i] - nums[i-1] - 1 # 与前一个之间需要补充的牌数
                    if diff > cnt0: return False # 大小王不够用
                    cnt0 -= diff
        return True
```

