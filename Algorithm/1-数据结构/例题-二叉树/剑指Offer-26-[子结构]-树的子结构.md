题目：[剑指 Offer 26. 树的子结构](https://leetcode.cn/problems/shu-de-zi-jie-gou-lcof/)

输入两棵二叉树A和B，判断B是不是A的子结构。(约定空树不是任意一个树的子结构)

B是A的子结构， 即 A中有出现和B相同的结构和节点值。

例如:
给定的树 A:

```
     3
    / \
   4   5
  / \
 1   2
```

给定的树 B：

```
   4 
  /
 1
```

返回 true，因为 B 与 A 的一个子树拥有相同的结构和节点值。

**示例 1：**

```
输入：A = [1,2,3], B = [3,1]
输出：false
```

**示例 2：**

```
输入：A = [3,4,5,1,2], B = [4,1]
输出：true
```

**限制：**

```
0 <= 节点个数 <= 10000
```

---

若树 B 是树 A 的子结构，则子结构的根节点可能为树 A 的任意一个节点。因此，判断树 B 是否是树 A 的子结构，需完成以下两步工作：

1. 先序遍历树 A 中的每个节点 n_A ；（对应函数 `isSubStructure(A, B)`）
2. 判断树 A 中 **以 n_A 为根节点的子树** 是否包含树 B 。（对应函数 `isSame(A, B)`）

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
    // 检查「A 中」是否包含 B
    bool isSubStructure(TreeNode* A, TreeNode* B) {
        // 如果 A 为空，无论 B 有没有，都返回 false
        if (A == nullptr) return false;

        // 此时 A 有值，但 B 为空，返回false
        if (B == nullptr) return false;

        // 此时 A B 都有值，检查从「A B 节点开始」是否有相同的结构
        if (isSame(A, B)) return true;

        // 如果从「A B 节点开始」没有相同结构，检查「A 的左右节点中」「其中一个」是否包含 B
        if (isSubStructure(A->left, B) || isSubStructure(A->right, B)) return true;

        return false;
    }

    // 检查从「A B 节点开始」是否有相同的结构
    bool isSame(TreeNode* A, TreeNode* B) {
        if (A == nullptr) {
            // 如果 A 为空，B 也为空，返回 true
            // 如果 A 为空，B 不为空，返回 false
            return B == nullptr ? true : false;
        } else {
            // 如果 A 有值，B 为空，返回 true
            // 如果 A 有值，B 有值，若两个值相等继续递归判断，不想等返回false
            if (B == nullptr) {
                return true;
            } else {
                if (A->val == B->val) {
                    // 当前节点值相等，且左右子树也「都」相同
                    return isSame(A->left, B->left) && isSame(A->right, B->right);
                } else {
                    return false;
                }
            }
        }
        return true;  // 实际不会走到这
    }
};
```

