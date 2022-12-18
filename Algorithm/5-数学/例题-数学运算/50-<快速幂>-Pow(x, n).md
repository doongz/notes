#### [50. Pow(x, n)](https://leetcode-cn.com/problems/powx-n/)

[题解](https://leetcode-cn.com/problems/powx-n/solution/powx-n-by-leetcode-solution/)

实现 [pow(*x*, *n*)](https://www.cplusplus.com/reference/valarray/pow/) ，即计算 `x` 的整数 `n` 次幂函数（即，`xn` ）。

```
示例 1：

输入：x = 2.00000, n = 10
输出：1024.00000

示例 2：

输入：x = 2.10000, n = 3
输出：9.26100

示例 3：

输入：x = 2.00000, n = -2
输出：0.25000
解释：2-2 = 1/22 = 1/4 = 0.25
```

**提示：**

- `-100.0 < x < 100.0`
- `-231 <= n <= 231-1`
- `-104 <= xn <= 104`

---

「快速幂算法」的本质是分治算法。举个例子，如果我们要计算 $$ x^{64} $$ ，我们可以按照下面的顺序，从 x 开始，**每次直接把上一次的结果进行平方**，计算 6 次就可以得到  $$ x^{64} $$的值，而不需要对 x 乘 63 次 x。

$$
x \rightarrow x^2 \rightarrow x^4 \rightarrow x^8 \rightarrow x^{16} \rightarrow x^{32} \rightarrow x^{64}
$$

再举一个例子，如果我们要计算$$ x^{77} $$，我们可以按照下面的顺序：

$$
x \rightarrow x^2 \rightarrow x^4 \rightarrow x^9 \rightarrow x^{19} \rightarrow x^{38} \rightarrow x^{77}
$$

在 1->2, 2->4, 19->38 这些步骤中，我们直接把上一次的结果进行平方，而在 4->9, 9->19, 38->77 这些步骤中(为奇数时)，我们把上一次的结果进行平方后，还要额外乘一个 x。

直接**从左到右进行推导看上去很困难**，因为在每一步中，我们不知道在将上一次的结果平方之后，还需不需要额外乘 x。但如果我们**从右往左看，分治的思想就十分明显了**：

- 当我们要计算  $$ x^{n} $$时，我们可以先递归地计算出  $$ y=x^{「n/2」} $$「n/2」代表向下取整
- 根据递归计算的结果，如果 n 为偶数，返回$$ y^{2} $$ ；如果 n 为奇数，返回$$ y^{2}*x $$
- 递归的边界为 n=0，任意数的 0 次方均为 1。

时间复杂度：O(log⁡n) ，因为每次递归都会使得指数减少一半

空间复杂度：O(log⁡n)，即为递归的层数。这是由于递归的函数调用会使用栈空间

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        def quickMul(N):
            if N == 0:
                return 1.0
            y = quickMul(N // 2)
            if N % 2 == 0:
                # 当 N 为偶数
                return y * y
            else:
                # 不管最初或者中间有个 N 是偶或者奇，倒数第二层一定会经历 N 为1，
                # 这个时候 y=quickMul(1 // 2) 为1，整个函数将返回 1 * 1 * x
                # x 就时这个时候引入进来的
                return y * y * x

        if n >= 0:
            return quickMul(n)
        else:
            return 1 / quickMul(-n)
```

另外一种写法，不用递归，用迭代。但是不会

时间复杂度：O(log⁡n)

**空间复杂度：O(1)**

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        def quickMul(N):
            ans = 1.0
            # 贡献的初始值为 x
            x_contribute = x
            # 在对 N 进行二进制拆分的同时计算答案
            while N > 0:
                if N % 2 == 1:
                    # 如果 N 二进制表示的最低位为 1，那么需要计入贡献
                    ans *= x_contribute
                # 将贡献不断地平方
                x_contribute *= x_contribute
                # 舍弃 N 二进制表示的最低位，这样我们每次只要判断最低位即可
                N //= 2
            return ans
        
        return quickMul(n) if n >= 0 else 1.0 / quickMul(-n)

```

