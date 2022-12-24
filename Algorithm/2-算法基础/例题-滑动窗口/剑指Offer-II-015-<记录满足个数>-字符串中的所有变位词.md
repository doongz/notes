题目：[剑指 Offer II 015. 字符串中的所有变位词](https://leetcode.cn/problems/VabMRr/)

给定两个字符串 `s` 和 `p`，找到 `s` 中所有 `p` 的 **变位词** 的子串，返回这些子串的起始索引。不考虑答案输出的顺序。

**变位词** 指字母相同，但排列不同的字符串。

```
示例 1：

输入: s = "cbaebabacd", p = "abc"
输出: [0,6]
解释:
起始索引等于 0 的子串是 "cba", 它是 "abc" 的变位词。
起始索引等于 6 的子串是 "bac", 它是 "abc" 的变位词。

示例 2：

输入: s = "abab", p = "ab"
输出: [0,1,2]
解释:
起始索引等于 0 的子串是 "ab", 它是 "ab" 的变位词。
起始索引等于 1 的子串是 "ba", 它是 "ab" 的变位词。
起始索引等于 2 的子串是 "ab", 它是 "ab" 的变位词。
```

**提示:**

- `1 <= s.length, p.length <= 3 * 104`
- `s` 和 `p` 仅包含小写字母

注意：本题与主站 438 题相同： https://leetcode-cn.com/problems/find-all-anagrams-in-a-string/

---

```cpp
class Solution {
public:
    vector<int> findAnagrams(string s, string p) {
        int n = s.size();
        int len = p.size();
        int l = 0;
        int r = 0;
        unordered_map<char, int> need;
        unordered_map<char, int> window;
        int cnt = 0;
        vector<int> ans;

        for (char c : p) {
            need[c]++;
        }

        while (r < n) {
            char r_char = s[r];
            if (need.count(r_char)) {
                window[r_char]++;
                if (window[r_char] == need[r_char]) {
                    cnt++;
                }
            }

            if (r - l + 1 > len) {
                char l_char = s[l];
                if (need.count(l_char)) {
                    if (window[l_char] == need[l_char]) {
                        cnt--;
                    }
                    window[l_char]--;
                }
                l++;
            }
            if (cnt == need.size()) {
                ans.push_back(l);
            }
            r++;
        }

        return ans;
    }
};
```

