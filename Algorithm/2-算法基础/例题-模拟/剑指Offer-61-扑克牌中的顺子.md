题目：[剑指 Offer 61. 扑克牌中的顺子](https://leetcode.cn/problems/bu-ke-pai-zhong-de-shun-zi-lcof/)

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

