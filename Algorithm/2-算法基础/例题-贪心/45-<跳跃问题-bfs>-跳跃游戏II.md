[45. 跳跃游戏 II](https://leetcode-cn.com/problems/jump-game-ii/)

[参考题解 bfs](https://leetcode-cn.com/problems/jump-game-ii/solution/xiang-jie-dp-tan-xin-shuang-zhi-zhen-jie-roh4/)

[参考题解 贪心](https://leetcode-cn.com/problems/jump-game-ii/solution/tan-xin-suan-fa-zhu-xing-jie-shi-python3-by-zhu_sh/)

给你一个非负整数数组 `nums` ，你最初位于数组的第一个位置。

数组中的每个元素代表你在该位置可以跳跃的最大长度。

你的目标是使用最少的跳跃次数到达数组的最后一个位置。

假设你总是可以到达数组的最后一个位置。

```
示例 1:

输入: nums = [2,3,1,1,4]
输出: 2
解释: 跳到最后一个位置的最小跳跃数是 2。
     从下标为 0 跳到下标为 1 的位置，跳 1 步，然后跳 3 步到达数组的最后一个位置。

示例 2:

输入: nums = [2,3,0,1,4]
输出: 2

```

**提示:**

- `1 <= nums.length <= 104`
- `0 <= nums[i] <= 1000`



## 方法一：贪心

目的：使用最少的步数到达最后一个位置

**贪心策略：第 i 步位置为「第 i-1 步前」的点中所能达到的「最远位置」**，通过每一步的最优解，更新全局最优解，这就是贪心

算法步骤：

1. 定义步数step=0，能达到的最远位置max_bound=0，和上一步到达的边界pre_end=0
2. 遍历数组，遍历范围[0,n-1)
   - 更新当前能达到的最远位置max_bound=max(max_bound,nums[i]+i)
   - 如果索引i 到达了上一步的边界pre_end即i==pre_end，则
     - 更新边界pre_end，令 pre_end 等于新的最远边界max_bound
     - 令步数 step 加一

**注意：不要去遍历最后一个位置**

因为当 i == pre_end == n-1 时，说明已经可以走到 n-1位置了。如果这个时候站在 n-1 位置再往后跳，就跳出去了

时间复杂度：`O(n)`

空间复杂度：`O(1)`

执行用时：4 ms, 在所有 C++ 提交中击败了99.59%的用户

内存消耗：16.1 MB, 在所有 C++ 提交中击败了75.74%的用户

```cpp
class Solution {
public:
    int jump(vector<int>& nums) {
        int n = nums.size();
        int max_bound = 0;  // 当前能达到的最远位置
        int pre_end = 0;    // 上一步到达的边界
        int step = 0;       // 跳跃次数

        for (int cur = 0; cur < n - 1; cur++) {
            max_bound = max(max_bound, cur + nums[cur]);
            if (cur == pre_end) {
                pre_end = max_bound;  // 重新起跳，这一次跳的最远边界为 max_bound
                step++;
            }
        }
        return step;
    }
};
```

## 方法二：bfs

![](../../img/45.png)

- 如果某一个作为 **起跳点** 的格子可以跳跃的距离是 3，那么表示后面 3 个格子都可以作为 **起跳点**
  - 可以对每一个能作为 **起跳点** 的格子都尝试跳一次，把 **能跳到最远的距离** 不断更新
- 记录 **跳跃** 次数（bfs 的深度），如果跳到了终点，就得到了结果

时间复杂度：`O(n^2)`，原数据的长度为 10^4，但是由于 visited 防止走重复的，勉强可以通过

空间复杂度：`O(n)`

执行用时：1904 ms, 在所有 C++ 提交中击败了5.04%的用户

内存消耗：401.2 MB, 在所有 C++ 提交中击败了5.04%的用户

```cpp
class Solution {
public:
    int jump(vector<int>& nums) {
        int n = nums.size();
        if (n == 1) return 0;

        // 构建邻接表
        unordered_map<int, vector<int>> adj;
        for (int i = 0; i < n; i++) {
            for (int j = 1; j <= nums[i]; j++) {
                if (i + j < n) adj[i].push_back(i + j);
            }
        }

        // bfs
        deque<int> queue = {0};
        unordered_set<int> visited;  // 记录已经走过的，防止下次再走
        int depth = 0;
        while (!queue.empty()) {
            int layerSz = queue.size();
            for (int i = 0; i < layerSz; i++) {
                int cur = queue.front();
                queue.pop_front();
                if (cur == n - 1) return depth;  // 到了最后一个，返回深度
                for (int next_node : adj[cur]) {
                    if (visited.count(next_node) == 0) {
                        queue.push_back(next_node);
                        visited.insert(next_node);
                    }
                }
            }
            depth++;
        }
        return depth;
    }
};
```

