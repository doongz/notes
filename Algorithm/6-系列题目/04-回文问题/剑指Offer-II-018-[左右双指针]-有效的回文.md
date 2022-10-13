题目：[剑指 Offer II 018. 有效的回文](https://leetcode.cn/problems/XltzEq/)

```c++
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

