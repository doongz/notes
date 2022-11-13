题目：[剑指 Offer II 017. 含有所有字符的最短字符串](https://leetcode.cn/problems/M1oyTv/)

给定两个字符串 `s` 和 `t` 。返回 `s` 中包含 `t` 的所有字符的最短子字符串。如果 `s` 中不存在符合条件的子字符串，则返回空字符串 `""` 。

如果 `s` 中存在多个符合条件的子字符串，返回任意一个。

**注意：** 对于 `t` 中重复字符，我们寻找的子字符串中该字符数量必须不少于 `t` 中该字符数量。

```
例 1：

输入：s = "ADOBECODEBANC", t = "ABC"
输出："BANC" 
解释：最短子字符串 "BANC" 包含了字符串 t 的所有字符 'A'、'B'、'C'

示例 2：

输入：s = "a", t = "a"
输出："a"

示例 3：

输入：s = "a", t = "aa"
输出：""
解释：t 中两个字符 'a' 均应包含在 s 的子串中，因此没有符合条件的子字符串，返回空字符串。
```

**提示：**

- `1 <= s.length, t.length <= 105`
- `s` 和 `t` 由英文字母组成

进阶：你能设计一个在 o(n) 时间内解决此问题的算法吗？

 注意：本题与主站 76 题相似（本题答案不唯一）：https://leetcode-cn.com/problems/minimum-window-substring/

```c++
class Solution {
public:
    string minWindow(string s, string t) {
        int n = s.size();
        int l = 0;
        int r = 0;
        unordered_map<char, int> need;
        unordered_map<char, int> window;
        int cnt = 0;
        // vector<vector<int>> ans;

        for (char c : t) {
            need[c]++;
        }
        int len = need.size();
        int left = -1;
        int right = -1;
        int min_len = INT_MAX;

        while (r < n) {
            char r_char = s[r];
            window[r_char]++;
            if (need.count(r_char) && window[r_char] == need[r_char]) {
                cnt++;
            }

            while (cnt == len) {
                // ans.push_back({l, r});
                if (r - l + 1 < min_len) {
                    min_len = r - l + 1;
                    left = l;
                    right = r;
                }

                char l_char = s[l];
                if (need.count(l_char) && window[l_char] == need[l_char]) {
                    cnt--;
                }
                window[l_char]--;
                l++;
            }
            r++;
        }
        // for (auto b : ans) {
        //     cout << b[0] << " " << b[1] << endl;
        // }
        if (min_len != INT_MAX) {
            // cout << s.substr(left, min_len) << endl;
            return s.substr(left, min_len);
        }

        return "";
    }
};
```

