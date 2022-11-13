题目：[剑指 Offer 29. 顺时针打印矩阵](https://leetcode.cn/problems/shun-shi-zhen-da-yin-ju-zhen-lcof/)

输入一个矩阵，按照从外向里以顺时针的顺序依次打印出每一个数字。

```
示例 1：

输入：matrix = [[1,2,3],[4,5,6],[7,8,9]]
输出：[1,2,3,6,9,8,7,4,5]

示例 2：

输入：matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
输出：[1,2,3,4,8,12,11,10,9,5,6,7]
```

**限制：**

- `0 <= matrix.length <= 100`
- `0 <= matrix[i].length <= 100`

注意：本题与主站 54 题相同：https://leetcode-cn.com/problems/spiral-matrix/

---

| 打印方向 | 1. 根据边界打印        | 2. 边界向内收缩 | 3. 是否打印完毕 |
| -------- | ---------------------- | --------------- | --------------- |
| 从左向右 | 左边界`l` ，右边界 `r` | 上边界 `t` 加 1 | 是否 `t > b`    |
| 从上向下 | 上边界 `t` ，下边界`b` | 右边界 `r` 减 1 | 是否 `l > r`    |
| 从右向左 | 右边界 `r` ，左边界`l` | 下边界 `b` 减 1 | 是否 `t > b`    |
| 从下向上 | 下边界 `b` ，上边界`t` | 左边界 `l` 加 1 | 是否 `l > r`    |



```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        if (len(matrix) == 0): return []
        rows = len(matrix)
        cols = len(matrix[0])
        l = 0
        r = cols - 1
        t = 0
        b = rows - 1
        ans = []
        
        while True:
            # left to right
            for i in range(l, r+1): ans.append(matrix[t][i])
            t += 1
            if t > b: break
            # top to bottom
            for i in range(t, b+1): ans.append(matrix[i][r])
            r -= 1
            if l > r: break
            # right to left
            for i in range(r, l-1, -1): ans.append(matrix[b][i])
            b -= 1
            if t > b: break
            # bottom to top
            for i in range(b, t-1, -1): ans.append(matrix[i][l])
            l += 1
            if l > r: break
        return ans

```

