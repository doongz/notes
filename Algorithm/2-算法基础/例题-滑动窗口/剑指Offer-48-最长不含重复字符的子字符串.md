题目：[剑指 Offer 48. 最长不含重复字符的子字符串](https://leetcode.cn/problems/zui-chang-bu-han-zhong-fu-zi-fu-de-zi-zi-fu-chuan-lcof/)

请从字符串中找出一个最长的不包含重复字符的子字符串，计算该最长子字符串的长度。

```
示例 1:

输入: "abcabcbb"
输出: 3 
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。

示例 2:

输入: "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。

示例 3:

输入: "pwwkew"
输出: 3
解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
     请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。
```

提示：

s.length <= 40000

注意：本题与主站 3 题相同：https://leetcode-cn.com/problems/longest-substring-without-repeating-characters/

---

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

