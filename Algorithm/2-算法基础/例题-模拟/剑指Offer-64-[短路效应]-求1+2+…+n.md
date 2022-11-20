题目：[剑指 Offer 64. 求1+2+…+n](https://leetcode.cn/problems/qiu-12n-lcof/)

题解：[面试题64. 求 1 + 2 + … + n（逻辑符短路，清晰图解）](https://leetcode.cn/problems/qiu-12n-lcof/solution/mian-shi-ti-64-qiu-1-2-nluo-ji-fu-duan-lu-qing-xi-/)

求 `1+2+...+n` ，要求不能使用乘除法、for、while、if、else、switch、case等关键字及条件判断语句（A?B:C）。

**示例 1：**

```
输入: n = 3
输出: 6
```

**示例 2：**

```
输入: n = 9
输出: 45
```

**限制：**

- `1 <= n <= 10000`

## 解题思路

本题在简单问题上做了许多限制，需要使用排除法一步步导向答案。

1+2+...+(n-1)+n 的计算方法主要有三种：平均计算、迭代、递归。

### **方法一：** 平均计算

**问题：** 此计算必须使用 **乘除法** ，因此本方法不可取，直接排除。

```python
def sumNums(n):
    return (1 + n) * n // 2
```

### **方法二：** 迭代

**问题：** 循环必须使用 while 或 for ，因此本方法不可取，直接排除。

```python
def sumNums(n):
    res = 0
    for i in range(1, n + 1):
        res += i
    return res
```

### **方法三：** 递归

**问题：** 终止条件需要使用 if ，因此本方法不可取。

```c++
class Solution {
public: 
    int dfs(int cur) {
        if (cur == 1) return 1;
        return cur + dfs(cur-1);
    }

    int sumNums(int n) {
        return dfs(n);
    }
};
```

**思考：** 除了 if 和 switch 等判断语句外，是否有其他方法可用来终止递归？

### 逻辑运算符的短路效应

![剑指64](../doc/剑指64.png)

常见的逻辑运算符有三种，即 “与 \&\& ”，“或 || ”，“非 ! ” ；而其有重要的短路效应，如下所示：

```c++
if(A && B)  // 若 A 为 false ，则 B 的判断不会执行（即短路），直接判定 A && B 为 false

if(A || B)  // 若 A 为 true ，则 B 的判断不会执行（即短路），直接判定 A || B 为 true
```

本题需要实现 “当 n = 1 时终止递归” 的需求，可通过短路效应实现。

```c++
n > 1 && sumNums(n - 1) // 当 n = 1 时 n > 1 不成立 ，此时 “短路” ，终止后续递归
```

将上述递归写法更新为：

```c++
class Solution {
public:
    int ans = 0;
    int dfs(int cur) {
        bool x = cur > 1 && dfs(cur-1);
        ans += cur;
        return 1;
    }

    int sumNums(int n) {
        dfs(n);
        return ans;
    }
};
```

