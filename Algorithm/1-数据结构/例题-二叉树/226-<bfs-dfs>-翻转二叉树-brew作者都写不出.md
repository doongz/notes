[226. 翻转二叉树](https://leetcode-cn.com/problems/invert-binary-tree/)

给你一棵二叉树的根节点 `root` ，翻转这棵二叉树，并返回其根节点。

**示例 1：**

![img](../../img/invert1-tree.jpg)

```
输入：root = [4,2,7,1,3,6,9]
输出：[4,7,2,9,6,3,1]
```

**提示：**

- 树中节点数目范围在 `[0, 100]` 内
- `-100 <= Node.val <= 100`

这个题画下图，一目了然

## 方法一：bfs

```cpp
class Solution {
public:
    TreeNode* invertTree(TreeNode* root) {
        if (!root) return nullptr;
        deque<TreeNode *> q{root};
        while (!q.empty()) {
            TreeNode *node = q.front();
            q.pop_front();
            TreeNode *tmp = node->left;
            node->left = node->right;
            node->right = tmp;
            if (node->left) q.push_back(node->left);
            if (node->right) q.push_back(node->right);
        }
        return root;
    }
};
```

```python
class Solution:
    def invertTree(self, root: TreeNode) -> TreeNode:

        if not root:
            return None
        
        queue = collections.deque()
        queue.append(root)
        while queue:
            cur = queue.popleft()
            cur.left, cur.right = cur.right, cur.left
            
            if cur.left:
                queue.append(cur.left)
            if cur.right:
                queue.append(cur.right)
        return root
```

## 方法二：dfs

```cpp
class Solution {
public:
    void dfs(TreeNode *node) {
        if (!node) return;
        TreeNode *tmp = node->left;
        node->left = node->right;
        node->right = tmp;
        dfs(node->left);
        dfs(node->right);
    }
    TreeNode* invertTree(TreeNode* root) {
        if (!root) return nullptr;
        dfs(root);
        return root;
    }
};
```

```python
class Solution:
    def invertTree(self, root: TreeNode) -> TreeNode:

        if not root:
            return None
        # 先序遍历 自顶向下
        def dfs(node):
            if not node:
                return None
            rightTree = node.right
            node.right = dfs(node.left)
            node.left = dfs(rightTree)
            return node

        return dfs(root)
```

