题目：[剑指 Offer II 017. 含有所有字符的最短字符串](https://leetcode.cn/problems/M1oyTv/)

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

