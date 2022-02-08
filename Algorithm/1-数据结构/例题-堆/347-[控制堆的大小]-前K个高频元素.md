[347. 前 K 个高频元素](https://leetcode-cn.com/problems/top-k-frequent-elements/)

## 方法：控制堆的大小

时间复杂度：`O(nlogk)`

空间复杂度：`O(n)`，unordered_map 为 `O(n)`，priority_queue 为 `O(k)`

```c++
class Solution {
public:
    struct cmpSmall {
        bool operator()(pair<int, int> &p1, pair<int, int> &p2) {
            return p1.second > p2.second;
        }
    };
    vector<int> topKFrequent(vector<int> &nums, int k) {
        unordered_map<int, int> um;
        for (int num : nums) {
            um[num]++;
        }

        priority_queue<pair<int, int>, vector<pair<int, int>>, cmpSmall> smallQ;
        for (auto it = um.begin(); it != um.end(); it++) {  // 注意：unordered_map的迭代器为向前迭代器
            if (smallQ.size() < k) {
                smallQ.push(*it);
            } else {
                if (it->second > smallQ.top().second) {
                    smallQ.pop();
                    smallQ.push(*it);
                }
            }
        }

        vector<int> ans;
        while (!smallQ.empty()) {
            ans.push_back(smallQ.top().first);
            smallQ.pop();
        }
        return ans;
    }
};
```

