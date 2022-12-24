[347. 前 K 个高频元素](https://leetcode-cn.com/problems/top-k-frequent-elements/)

给你一个整数数组 `nums` 和一个整数 `k` ，请你返回其中出现频率前 `k` 高的元素。你可以按 **任意顺序** 返回答案。

**示例 1:**

```
输入: nums = [1,1,1,2,2,3], k = 2
输出: [1,2]
```

**示例 2:**

```
输入: nums = [1], k = 1
输出: [1]
```

提示：

1 <= nums.length <= 105
k 的取值范围是 [1, 数组中不相同的元素的个数]
题目数据保证答案唯一，换句话说，数组中前 k 个高频元素的集合是唯一的

**进阶：**你所设计算法的时间复杂度 **必须** 优于 `O(n log n)` ，其中 `n` 是数组大小。

## 方法：控制堆的大小

时间复杂度：`O(nlogk)`

空间复杂度：`O(n)`，unordered_map 为 `O(n)`，priority_queue 为 `O(k)`

```cpp
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

