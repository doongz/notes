题目：[剑指 Offer II 018. 有效的回文](https://leetcode.cn/problems/XltzEq/)

给定一个字符串 `s` ，验证 `s` 是否是 **回文串** ，只考虑字母和数字字符，可以忽略字母的大小写。

本题中，将空字符串定义为有效的 **回文串** 。

```
示例 1:

输入: s = "A man, a plan, a canal: Panama"
输出: true
解释："amanaplanacanalpanama" 是回文串

示例 2:

输入: s = "race a car"
输出: false
解释："raceacar" 不是回文串
```

**提示：**

- `1 <= s.length <= 2 * 105`
- 字符串 `s` 由 ASCII 字符组成

注意：本题与主站 125 题相同： https://leetcode-cn.com/problems/valid-palindrome/



---

```cpp
class Solution {
public:
    bool is_char(char c) {
        if (97 <= c && c <= 122) return true;
        if (65 <= c && c <= 90) return true;
        if (48 <= c && c <= 57) return true;
        return false;
    }
    bool is_same(char a, char b) {
        if (97 <= a && a <= 122) a -= 32;
        if (97 <= b && b <= 122) b -= 32;
        return a == b;
    }

    bool isPalindrome(string s) {
        int l = 0;
        int r = s.size() - 1;
        while (l < r) {
            while (l < r && !is_char(s[l])) {
                l++;
            }
            while (l < r && !is_char(s[r])) {
                r--;
            }
            if (l < r && !is_same(s[l], s[r])) {
                // cout << l << " " << r << endl;
                return false;
            }
            l++;
            r--;
        }

        return true;
    }
};
```

