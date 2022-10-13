题目：[剑指 Offer II 019. 最多删除一个字符得到回文](https://leetcode.cn/problems/RQku0D/)

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

