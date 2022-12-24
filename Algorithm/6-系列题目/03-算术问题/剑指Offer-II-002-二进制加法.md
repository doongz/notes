题目：[剑指 Offer II 002. 二进制加法](https://leetcode.cn/problems/JFETK5/)

题解：[【负雪明烛】二进制加法详解：「模拟法」的技巧与细节](https://leetcode.cn/problems/JFETK5/solution/fu-xue-ming-zhu-er-jin-zhi-jia-fa-xiang-bu5dt/)

给定两个 01 字符串 `a` 和 `b` ，请计算它们的和，并以二进制字符串的形式输出。

输入为 **非空** 字符串且只包含数字 `1` 和 `0`。

```
示例 1:

输入: a = "11", b = "10"
输出: "101"

示例 2:

输入: a = "1010", b = "1011"
输出: "10101"
```

提示：

每个字符串仅由字符 '0' 或 '1' 组成。
1 <= a.length, b.length <= 10^4
字符串如果不是 "0" ，就都不含前导零。

注意：本题与主站 67 题相同：https://leetcode-cn.com/problems/add-binary/

## 二进制加法

二进制加法的计算也可以采用类似的方法，与十进制不同的是，**二进制的进位规则是「逢二进一」**，即当求和结果 >= 2>=2 时，需要向前进位。

在代码中需要注意的有：

- 本题给出的二进制数字是字符串形式，不可以转化成 int 型，因为**可能溢出**；
- 两个「**加数**」的字符串长度可能不同；
- 在最后，如果进位 carry 不为 0，那么**最后需要计算进位**；
- 向结果字符串 res 拼接的顺序是向后拼接，**返回时需要把 res 反转** 。

`while (i >= 0 || j >= 0 || carry != 0)`含义：

- 字符串 `a` 和 `b` 只要有一个没遍历完，那么就继续遍历；
- 如果字符串 `a` 和 `b` 都遍历完了，但是最后留下的进位 `carry != 0`，那么需要把进位也保留到结果中。

取 digit 的时候，如果字符串 a 和 b 中有一个已经遍历完了（即 i <= 0 或者 j <= 0），则认为 a 和 b 的对应位置是 0 。

```cpp
class Solution {
public:
    string addBinary(string a, string b) {
        string ans = "";       // 返回结果
        int i = a.size() - 1;  // 标记遍历到 a 的位置
        int j = b.size() - 1;  // 标记遍历到 b 的位置
        int carry = 0;         // 进位

        while (i >= 0 || j >= 0 || carry != 0) {   // a 没遍历完，或 b 没遍历完，或进位不为 0
            int digitA = i >= 0 ? a[i] - '0' : 0;  // 当前 a 的取值
            int digitB = j >= 0 ? b[j] - '0' : 0;  // 当前 b 的取值
            int sum = digitA + digitB + carry;     // 当前位置相加的结果
            carry = sum >= 2 ? 1 : 0;              // 是否有进位
            sum = sum >= 2 ? sum - 2 : sum;        // 去除进位后留下的数字
            ans += (sum + '0');                    // 把去除进位后留下的数字拼接到结果中
            i--;                                   // 遍历到 a 的位置向左移动
            j--;                                   // 遍历到 b 的位置向左移动
        }
        reverse(ans.begin(), ans.end());  // 把结果反转并返回
        return ans;
    }
};

```

