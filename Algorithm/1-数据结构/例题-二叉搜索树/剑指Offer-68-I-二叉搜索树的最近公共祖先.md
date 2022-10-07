题目：[剑指 Offer 68 - I. 二叉搜索树的最近公共祖先](https://leetcode.cn/problems/er-cha-sou-suo-shu-de-zui-jin-gong-gong-zu-xian-lcof/)

p,q 与 rootroot 的子树关系，即：

- 若 root.val < p.val ，则 pp 在 root 右子树 中；
- 若 root.val > p.val ，则 pp 在 root 左子树 中；
- 若 root.val = p.val ，则 pp 和 root 指向 同一节点 。

#### 方法一：迭代

**循环搜索**：当节点 root 为空时跳出；

- 当 p, q 都在 root 的 右子树 中，则遍历至 root.right；
- 否则，当 p, q 都在 root 的 左子树 中，则遍历至 root.left；
- 否则，说明找到了 最近公共祖先 ，跳出。

**返回值**： 最近公共祖先 root。

**复杂度分析**：

- 时间复杂度 O(N)： 其中 N 为二叉树节点数；每循环一轮排除一层，二叉搜索树的层数最小为 logN （满二叉树），最大为 N （退化为链表）。
- 空间复杂度 O(1)： 使用常数大小的额外空间。

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
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        while (root) {
            if (root->val < p->val && root->val < q->val) {
                // p,q 都在 root 的右子树中
                root = root->right;
            } else if (root->val > p->val && root->val > q->val) {
                // p,q 都在 root 的左子树中
                root = root->left;
            } else {
                // 不满足上述两个条件，说明 p,q 分叉了
                break;
            }
        }
        return root;
    }
};
```

#### 方法二：递归

**递推工作**：

- 当 p, q 都在 root 的 右子树 中，则开启递归 root.right 并返回；
- 否则，当 p, q 都在 root 的 左子树 中，则开启递归 root.left 并返回；

**返回值**： 最近公共祖先 root 。

**复杂度分析**：

- 时间复杂度 O(N)： 其中 N 为二叉树节点数；每循环一轮排除一层，二叉搜索树的层数最小为 logN （满二叉树），最大为 N （退化为链表）。
- 空间复杂度 O(N)： 最差情况下，即树退化为链表时，递归深度达到树的层数 N。

```c++
class Solution {
public:
    TreeNode* dfs(TreeNode* cur, TreeNode* p, TreeNode* q) {
        if (cur->val < p->val && cur->val < q->val) {
            return dfs(cur->right, p, q);
        } else if (cur->val > p->val && cur->val > q->val) {
            return dfs(cur->left, p, q);
        }
        return cur;
    }

    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        return dfs(root, p, q);
    }
};
```

