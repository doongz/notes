题目：[剑指 Offer II 015. 字符串中的所有变位词](https://leetcode.cn/problems/VabMRr/)

```c++
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

