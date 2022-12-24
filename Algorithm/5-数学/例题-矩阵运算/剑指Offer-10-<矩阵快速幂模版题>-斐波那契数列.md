题目：[剑指 Offer 10- I. 斐波那契数列](https://leetcode.cn/problems/fei-bo-na-qi-shu-lie-lcof/)

写一个函数，输入 n ，求斐波那契（Fibonacci）数列的第 n 项（即 F(N)）。斐波那契数列的定义如下：

```
F(0) = 0,   F(1) = 1
F(N) = F(N - 1) + F(N - 2), 其中 N > 1.
```

斐波那契数列由 0 和 1 开始，之后的斐波那契数就是由之前的两数相加而得出。

答案需要取模 1e9+7（1000000007），如计算初始结果为：1000000008，请返回 1。

**示例 1：**

```
输入：n = 2
输出：1
```

**示例 2：**

```
输入：n = 5
输出：5
```

**提示：**

- `0 <= n <= 100`

---

**1、利用题目给定的依赖关系，对目标矩阵元素进行展开**：

形如 `f(n) = f(n - 1) + f(n - 2)` 展开 `2*1` 矩阵，注意只能使用 `f(n) f(n-1) f(n-2)` 三个元素

```
#define N 2

f(n)      1*f(n-1) + 1*f(n-2)
       =
f(n-1)    1*f(n-1) + 0*f(n-2)
```

**2、求 Mat 矩阵**

那么根据矩阵乘法，即有：

```
f(n)      1 1   f(n-1)
       =      *
f(n-1)    1 0   f(n-2)
```

即 Mat 矩阵为

```
1 1
1 0
```

**3、利用 `Mat` 实现数列递推**

```
f(n)         		 f(1)
       = Mat^(n-1) *
f(n-1)       		 f(0)
```

**4、计算**

通过「矩阵快速幂」计算出 `Mat^(n-1)` 为 `res` 矩阵

答案就是

```
	   f(1)
res * 
	   f(0)
	   
return res[0][0]*f(1) + res[0][1]*f(0);
```



```cpp
#define N 2
class Solution {
public:
    int mod = 1e9 + 7;

    vector<vector<long>> multiply(vector<vector<long>>& a, vector<vector<long>>& b) {
        vector<vector<long>> c(N, vector<long>(N, 0));
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                for (int k = 0; k < N; k++) {
                    c[i][j] += a[i][k] * b[k][j];
                }
                c[i][j] %= mod;
            }
        }
        return c;
    }

    int fib(int n) {
        if (n == 0) return 0;
        if (n == 1) return 1;

        vector<vector<long>> res = {
            {1, 0},
            {0, 1}
        };
        vector<vector<long>> mat = {
            {1, 1},
            {1, 0}
        };

        // 快速幂
        int k = n - 1;
        while (k > 0) {
            if ((k & 1) != 0) res = multiply(mat, res);
            mat = multiply(mat, mat);
            k >>= 1;
        }
        return res[0][0];
    }
};
```



