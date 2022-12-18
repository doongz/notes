[692. 前K个高频单词](https://leetcode-cn.com/problems/top-k-frequent-words/)

给定一个单词列表 `words` 和一个整数 `k` ，返回前 `k` 个出现次数最多的单词。

返回的答案应该按单词出现频率由高到低排序。如果不同的单词有相同出现频率， **按字典顺序** 排序。

```
示例 1：

输入: words = ["i", "love", "leetcode", "i", "love", "coding"], k = 2
输出: ["i", "love"]
解析: "i" 和 "love" 为出现次数最多的两个单词，均为2次。
    注意，按字母顺序 "i" 在 "love" 之前。
    
示例 2：

输入: ["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], k = 4
输出: ["the", "is", "sunny", "day"]
解析: "the", "is", "sunny" 和 "day" 是出现次数最多的四个单词，
    出现次数依次为 4, 3, 2 和 1 次。

```

注意：

1 <= words.length <= 500
1 <= words[i] <= 10
words[i] 由小写英文字母组成。
k 的取值范围是 [1, 不同 words[i] 的数量]

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

