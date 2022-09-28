题目：[剑指 Offer 48. 最长不含重复字符的子字符串](https://leetcode.cn/problems/zui-chang-bu-han-zhong-fu-zi-fu-de-zi-zi-fu-chuan-lcof/)

```c++
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        int n = s.size();
        int r = 0;
        int l = 0;
        unordered_map<char, int> window;
        int ans = 0;

        while (r < n) {
            char cur = s[r];
            window[cur]++;

            while (window[cur] > 1 && l < r) {
                window[s[l]]--;
                l++;
            }
            ans = max(ans, r - l + 1);
            r++;
        }

        return ans;
    }
};
```

