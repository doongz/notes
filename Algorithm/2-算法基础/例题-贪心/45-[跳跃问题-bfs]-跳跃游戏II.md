[45. 跳跃游戏 II](https://leetcode-cn.com/problems/jump-game-ii/)

[参考题解 bfs](https://leetcode-cn.com/problems/jump-game-ii/solution/xiang-jie-dp-tan-xin-shuang-zhi-zhen-jie-roh4/)

[参考题解 贪心](https://leetcode-cn.com/problems/jump-game-ii/solution/tan-xin-suan-fa-zhu-xing-jie-shi-python3-by-zhu_sh/)

## 方法一：bfs

<img src="../doc/45.png" alt="45" style="zoom:30%;" />

- 如果某一个作为 **起跳点** 的格子可以跳跃的距离是 3，那么表示后面 3 个格子都可以作为 **起跳点**
  - 可以对每一个能作为 **起跳点** 的格子都尝试跳一次，把 **能跳到最远的距离** 不断更新
- 记录 **跳跃** 次数（bfs 的深度），如果跳到了终点，就得到了结果

时间复杂度：`O(n^2)`，原数据的长度为 10^4，但是由于 visited 防止走重复的，勉强可以通过

空间复杂度：`O(n)`

执行用时：1904 ms, 在所有 C++ 提交中击败了5.04%的用户

内存消耗：401.2 MB, 在所有 C++ 提交中击败了5.04%的用户

```c++
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

## 方法二：贪心

目的：使用最少的步数到达最后一个位置

**贪心策略：第 i 步位置为「第 i-1 步前」的点中所能达到的「最远位置」**

算法步骤：

1. 定义步数step=0，能达到的最远位置max\_bound=0，和上一步到达的边界end=0
2. 遍历数组，遍历范围[0,n-1)
   - 更新当前能达到的最远位置max\_bound=max(max\_bound,nums[i]+i)
   - 如果索引i 到达了上一步的边界end，即i==end，则
     - 更新边界end，令 end 等于新的最远边界max\_bound
     - 令步数 step 加一

**注意：不要去遍历最后一个位置**，和 55 题思路上略有不同（由于 max() 的位置引起的）

因为当 i == end == n-1 时，说明上一次已经可以走到 n-1位置了

如果这个时候站在 n-1 位置再往后跳，就跳出去了

时间复杂度：`O(n)`

空间复杂度：`O(1)`

```c++
class Solution {
public:
    int jump(vector<int>& nums) {
        int n = nums.size();
        int max_bound = 0;  // 当前能达到的最远位置
        int end = 0;        // 上一步到达的边界
        int step = 0;       // 跳跃次数

        for (int i = 0; i < n - 1; i++) {
            max_bound = max(max_bound, i + nums[i]);
            if (i == end) {
                end = max_bound;  // 重新起跳，这一次跳的最远边界为 max_bound
                step++;
            }
        }
        return step;
    }
};
```

