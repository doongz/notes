题目：[57. 插入区间](https://leetcode.cn/problems/insert-interval/)

给你一个 **无重叠的** *，*按照区间起始端点排序的区间列表。

在列表中插入一个新的区间，你需要确保列表中的区间仍然有序且不重叠（如果有必要的话，可以合并区间）。

```
示例 1：

输入：intervals = [[1,3],[6,9]], newInterval = [2,5]
输出：[[1,5],[6,9]]

示例 2：

输入：intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
输出：[[1,2],[3,10],[12,16]]
解释：这是因为新的区间 [4,8] 与 [3,5],[6,7],[8,10] 重叠。

示例 3：

输入：intervals = [], newInterval = [5,7]
输出：[[5,7]]

示例 4：

输入：intervals = [[1,5]], newInterval = [2,3]
输出：[[1,5]]

示例 5：

输入：intervals = [[1,5]], newInterval = [2,7]
输出：[[1,7]]
```

提示：

0 <= intervals.length <= 104
intervals[i].length == 2
0 <= intervals[i][0] <= intervals[i][1] <= 105
intervals 根据 intervals[i][0] 按 升序 排列
newInterval.length == 2
0 <= newInterval[0] <= newInterval[1] <= 105

---

本题中的区间已经按照起始端点升序排列，因此我们直接遍历区间列表，寻找新区间的插入位置即可。具体步骤如下：

1. 首先将新区间左边且相离的区间加入结果集（遍历时，如果当前区间的结束位置小于新区间的开始位置，说明当前区间在新区间的左边且相离）；
2. 接着判断当前区间是否与新区间重叠，重叠的话就进行合并，直到遍历到当前区间在新区间的右边且相离，将最终合并后的新区间加入结果集；
3. 最后将新区间右边且相离的区间加入结果集。

```c++
class Solution {
public:
    vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& newInterval) {
        vector<vector<int>> ans;
        int n = intervals.size();
        int i = 0;
        // 遍历区间列表：
        // 首先将新区间左边且相离的区间加入结果集
        while (i < n && intervals[i][1] < newInterval[0]) {
            ans.push_back(intervals[i]);
            i++;
        }

        // 接着判断当前区间是否与新区间重叠，重叠的话就进行合并，直到遍历到当前区间在新区间的右边且相离，
        // 将最终合并后的新区间加入结果集
        while(i < n && intervals[i][0] <= newInterval[1]) {
            newInterval[0] = min(intervals[i][0], newInterval[0]);
            newInterval[1] = max(intervals[i][1], newInterval[1]);
            i++;
        }
        ans.push_back(newInterval);

        // 最后将新区间右边且相离的区间加入结果集
        while(i < n) {
            ans.push_back(intervals[i]);
            i++;
        }
        return ans;
    }
};
```

