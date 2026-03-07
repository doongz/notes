[101. 对称二叉树](https://leetcode-cn.com/problems/symmetric-tree/)

给你一个二叉树的根节点 `root` ， 检查它是否轴对称。

**示例 1：**

![img](../../img/symtree1.jpg)

## 方法一：dfs

如果一个树的左子树与右子树镜像对称，那么这个树是对称的。

因此，该问题可以转化为：两个树在什么情况下互为镜像？

如果同时满足下面的条件，两个树互为镜像：

它们的两个根结点具有相同的值
每个树的右子树都与另一个树的左子树镜像对称

我们可以实现这样一个递归函数，通过「同步移动」两个指针的方法来遍历这棵树，p 指针和 q 指针一开始都指向这棵树的根，随后 p 右移时，q 左移，p 左移时，q 右移。每次检查当前 p 和 q 节点的值是否相等，如果相等再判断左右子树是否对称。



```cpp
class Solution {
public:
    bool dfs(TreeNode* p1, TreeNode* p2) {
        if (!p1 && !p2) return true;
        if (!p1 || !p2) return false;
        return (p1->val == p2->val) && dfs(p1->left, p2->right) && dfs(p1->right, p2->left);
    }
    bool isSymmetric(TreeNode* root) {
        return dfs(root->left, root->right);
    }
};
```

## 方法二：bfs

```c++
class Solution {
public:
    bool check(const vector<int>& layer) {
        int n = layer.size();
        for (int i=0;i<(n/2);i++) {
            if (layer[i] != layer[n-i-1]) return false;
        }
        return true;
    }
    bool isSymmetric(TreeNode* root) {
        deque<TreeNode*> q = {root};
        while (!q.empty()) {
            vector<int> layer;
            int size = q.size();
            for (int i=0;i<size;i++) {
                TreeNode* node = q.front();
                layer.push_back(node->val);
                q.pop_front();
                if (node->val == 9999) continue;
                if (node->left) {
                    q.push_back(node->left);
                } else {
                    TreeNode* tmp = new TreeNode(9999);
                    q.push_back(tmp);
                }
                if (node->right) {
                    q.push_back(node->right);
                } else {
                    TreeNode* tmp = new TreeNode(9999);
                    q.push_back(tmp);
                }
            }
            if (!check(layer)) return false;
        }
        return true;
    }
};
```



```cpp
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

