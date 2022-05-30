题目：[863. 二叉树中所有距离为 K 的结点](https://leetcode.cn/problems/all-nodes-distance-k-in-binary-tree/)

## 方法：dfs+bfs

dfs遍历二叉树，生成图的临接表

根据临近表，bfs遍历，从 target 到第 k 层

第 k 层，退出的时候，队列里面就是第 k 层的所有节点

时间复杂度：`O(n)`，dfs 和 bfs 都是`O(n)`

空间复杂度：`O(n)`，dfs 和 bfs 都是`O(n)`

```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Solution {
public:
    vector<vector<int>> adj;

    void dfs(TreeNode* node) {
        if (node->left) {
            adj[node->val].push_back(node->left->val);
            adj[node->left->val].push_back(node->val);
            dfs(node->left);
        }
        if (node->right) {
            adj[node->val].push_back(node->right->val);
            adj[node->right->val].push_back(node->val);
            dfs(node->right);
        }
    }

    vector<int> distanceK(TreeNode* root, TreeNode* target, int k) {
        adj.resize(501);
        dfs(root);  // 生成临接表
        // for (auto a : adj) {
        //     for (auto b : a) cout << b << " ";
        //     cout << endl;
        // }

        deque<int> que = {target->val};
        unordered_set<int> visited = {target->val};  // 不走回头路
        int depth = 0;
        while (!que.empty()) {
            if (depth == k) break;

            int sz = que.size();
            for (int i = 0; i < sz; i++) {
                int cur = que.front();
                que.pop_front();
                for (int next : adj[cur]) {
                    if (visited.count(next) == 1) continue;
                    que.push_back(next);
                    visited.insert(next);
                }
            }
            depth++;
        }

        vector<int> ans;
        for (int num : que) {
            ans.push_back(num);
        }
        return ans;
    }
};
```

