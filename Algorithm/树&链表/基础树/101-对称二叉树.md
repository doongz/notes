[101. 对称二叉树](https://leetcode-cn.com/problems/symmetric-tree/)

## 方法一：dfs

```c++
class Solution {
public:
    bool dfs(TreeNode *l, TreeNode *r) {
        if (!l && !r) return true;
        if (!l || !r) return false;
        return l->val == r->val && dfs(l->left, r->right) && dfs(l->right, r->left);
    }
    bool isSymmetric(TreeNode *root) {
        return dfs(root, root);
    }
};
```

## 方法二：bfs

```c++
class Solution {
public:
    bool isSymmetric(TreeNode *root) {
        queue<TreeNode *> q;
        q.push(root);
        q.push(root);
        
        while (!q.empty()) {
            TreeNode *l = q.front(); q.pop();
            TreeNode *r = q.front(); q.pop();
            if (!l && !r) continue;
            if (!l || !r) return false;
            if (l->val != r->val) return false;

            q.push(l->left);
            q.push(r->right);
            q.push(l->right);
            q.push(r->left);
        }
        return true;
    }
};
```

