题目：[剑指 Offer II 019. 最多删除一个字符得到回文](https://leetcode.cn/problems/RQku0D/)

给定一个非空字符串 `s`，请判断如果 **最多** 从字符串中删除一个字符能否得到一个回文字符串。

```
示例 1:

输入: s = "aba"
输出: true

示例 2:

输入: s = "abca"
输出: true
解释: 可以删除 "c" 字符 或者 "b" 字符

示例 3:

输入: s = "abc"
输出: false
```

**提示:**

- `1 <= s.length <= 105`
- `s` 由小写英文字母组成

注意：本题与主站 680 题相同： https://leetcode-cn.com/problems/valid-palindrome-ii/



```c++
class Solution {
public:
    string str;
    bool is_same(int l, int r) {
        while (l < r) {
            if (str[l] != str[r]) return false;
            l++;
            r--;
        }
        return true;
    }
    bool validPalindrome(string s) {
        str = s;
        int l = 0;
        int r = str.size() - 1;
        while (l < r) {
            if (str[l] != str[r]) {
                if (is_same(l + 1, r) || is_same(l, r - 1)) {
                    return true;
                }
                return false;
            }
            l++;
            r--;
        }
        return true;
    }
};
```

