题目：[剑指 Offer II 016. 不含重复字符的最长子字符串](https://leetcode.cn/problems/wtcaE1/)

```c++
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        int n = s.size();
        int l = 0;
        int r = 0;
        unordered_set<char> windows;
        int ans = 0;

        while (r < n) {
            char r_char = s[r];
            while (windows.count(r_char)) {
                windows.erase(s[l]);
                l++;
            }
            windows.insert(r_char);
            ans = max(ans, r - l + 1);
            r++;
        }
        return ans;
    }
};
```

