题目：[剑指 Offer II 034. 外星语言是否排序](https://leetcode.cn/problems/lwyVBB/)

```c++
class Solution {
public:
    vector<int> order_map;

    bool cmp(string &w1, string &w2) {
        // <= return true
        int n = min(w1.size(), w2.size());
        for (int i = 0; i < n; i++) {
            // cout << i << ": " << w1[i] << "," << w2[i] << endl;
            int idx1 = order_map[w1[i]-'a'];
            int idx2 = order_map[w2[i]-'a'];
            if (idx1 < idx2) {
                return true;
            } else if (idx1 > idx2) {
                return false;
            }
        }
        if (w1.size() == n && w2.size() == n) return true;
        if (w1.size() > n) return false;
        return true;
    }
    bool isAlienSorted(vector<string>& words, string order) {
        order_map.resize(26, 0);
        for (int i = 0; i < 26; i++) {
            order_map[order[i] - 'a'] = i;
        }
        int n = words.size();
        for (int i = 0; i < n - 1; i++) {
            if (!cmp(words[i], words[i+1])) {
                return false;
            }
            // cout << "**********" << endl;
        }
        return true;
    }
};
```

