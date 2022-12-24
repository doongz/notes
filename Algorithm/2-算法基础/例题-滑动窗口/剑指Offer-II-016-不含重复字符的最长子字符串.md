题目：[剑指 Offer II 016. 不含重复字符的最长子字符串](https://leetcode.cn/problems/wtcaE1/)

给定一个字符串 `s` ，请你找出其中不含有重复字符的 **最长连续子字符串** 的长度。

```
示例 1:

输入: s = "abcabcbb"
输出: 3 
解释: 因为无重复字符的最长子字符串是 "abc"，所以其长度为 3。

示例 2:

输入: s = "bbbbb"
输出: 1
解释: 因为无重复字符的最长子字符串是 "b"，所以其长度为 1。

示例 3:

输入: s = "pwwkew"
输出: 3
解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
     请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。

示例 4:

输入: s = ""
输出: 0
```

**提示：**

- `0 <= s.length <= 5 * 104`
- `s` 由英文字母、数字、符号和空格组成

注意：本题与主站 3 题相同： https://leetcode-cn.com/problems/longest-substring-without-repeating-characters/

```cpp
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

