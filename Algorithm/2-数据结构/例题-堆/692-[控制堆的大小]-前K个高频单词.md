[692. 前K个高频单词](https://leetcode-cn.com/problems/top-k-frequent-words/)

## 方法：控制堆的大小

时间复杂度：`O(nlogk)`

空间复杂度：`O(n)`

**重点学习下官方的写法**

```c++
class Solution {
public:
    vector<string> topKFrequent(vector<string> &words, int k) {
        unordered_map<string, int> um;
        for (int i = 0; i < words.size(); i++) {
            um[words[i]]++;
        }

        // 小根堆
        auto cmp = [&](const auto &a, const auto &b) {
            return a.second == b.second ? a.first < b.first : a.second > b.second;
            // if (a.second != b.second) {
            //     return a.second > b.second;
            // } else {
            //     return a.first < b.first;
            // }
        };
        priority_queue<pair<string, int>, vector<pair<string, int>>, decltype(cmp)> smallQ(cmp);
        for (auto& it : um) {
            smallQ.push(it);
            if (smallQ.size() > k) {
                smallQ.pop();
            }
        }

        vector<string> ans(k);
        for (int i = k - 1; i >= 0;i--) {
            ans[i] = (smallQ.top().first);
            smallQ.pop();
        }
        return ans;
    }
};

```

