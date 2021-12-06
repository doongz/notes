#### [69. Sqrt(x)](https://leetcode-cn.com/problems/sqrtx/)

**[二分法](https://leetcode-cn.com/problems/sqrtx/solution/x-de-ping-fang-gen-by-leetcode-solution/)**

跳出来的时候一定是在平方根附近的，最后判断一下如果平方大于x的话就返回它前面的一个值，否则就正常返回就行了

时间复杂度：O(logx)

空间复杂度：O(1)

```python
class Solution:
    def mySqrt(self, x: int) -> int:
        l = 0
        r = x
        while l <= r:
            mid = l + (r - l) // 2
            tmp = mid * mid
            if tmp == x:
                return mid
            elif tmp < x:
                l = mid + 1
            else:
                r = mid - 1

        return mid-1 if mid * mid > x else mid
```

**[牛顿迭代法](https://leetcode-cn.com/problems/sqrtx/solution/x-de-ping-fang-gen-by-leetcode-solution/)**

预备知识：[泰勒计数](https://zh.wikipedia.org/wiki/%E6%B3%B0%E5%8B%92%E7%BA%A7%E6%95%B0) [牛顿迭代法](https://baike.baidu.com/item/%E7%89%9B%E9%A1%BF%E8%BF%AD%E4%BB%A3%E6%B3%95)
