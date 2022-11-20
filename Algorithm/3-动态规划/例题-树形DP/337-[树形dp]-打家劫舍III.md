题目：[337. 打家劫舍 III](https://leetcode-cn.com/problems/house-robber-iii/)

小偷又发现了一个新的可行窃的地区。这个地区只有一个入口，我们称之为 root 。

除了 root 之外，每栋房子有且只有一个“父“房子与之相连。一番侦察之后，聪明的小偷意识到“这个地方的所有房屋的排列类似于一棵二叉树”。 如果 两个直接相连的房子在同一天晚上被打劫 ，房屋将自动报警。

给定二叉树的 root 。返回 在不触动警报的情况下 ，小偷能够盗取的最高金额 。

![rob1-tree](../doc/rob1-tree.jpeg)

```
输入: root = [3,2,3,null,3,null,1]
输出: 7 
解释: 小偷一晚能够盗取的最高金额 3 + 3 + 1 = 7
```

![rob2-tree](../doc/rob2-tree.jpeg)

```
输入: root = [3,4,5,1,3,null,1]
输出: 9
解释: 小偷一晚能够盗取的最高金额 4 + 5 = 9
```

**提示：**

- 树的节点数在 `[1, 104]` 范围内
- `0 <= Node.val <= 104`

---

关键：当前结点「偷」或者「不偷」决定了孩子结点偷或者不偷，把这一点设计成状态，放在第 2 维，这一步叫「消除后效性」，这一点技巧非常常见。

**1. 定义状态**

`dp[node][j]` ：这里 node 表示一个结点，以 node 为根结点的树，并且规定了 node 是否偷取能够获得的最大价值。

- j = 0 位置，记录 node 结点「不偷取」可得的最大价值；
- j = 1 位置，记录 node 结点「偷取」可得的最大价值；

**2. 状态转移方程**

根据当前结点偷或者不偷，就决定了需要从哪些**子结点**里的对应的状态转移过来。

- 如果当前结点不偷，左右子结点偷或者不偷都行，选最大者；
- 如果当前结点偷，左右子结点均不能偷。

**3. 初始化**

一个结点都没有，空节点，返回 {0, 0}，对应后序遍历时候的递归终止条件；

**4. 输出**

在根结点的时候，返回两个状态的较大者。

**空间优化**

优化不了

**复杂度分析**

时间复杂度：`O(n)`

空间复杂度：`O(n)`，每个节点都有一个 dp 数组

```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    vector<int> dfs(TreeNode* cur) {
        if (cur == nullptr) return {0, 0};

        vector<int> left = dfs(cur->left);
        vector<int> right = dfs(cur->right);

        vector<int> dp(2, 0);
        dp[0] = max(left[0], left[1]) + max(right[0], right[1]);  // 当前结点不偷
        dp[1] = cur->val + left[0] + right[0];                    // 当前结点偷了
        return dp;
    }
    int rob(TreeNode* root) {
        vector<int> res = dfs(root);
        return max(res[0], res[1]);
    }
};
```



