题目：[剑指 Offer 55 - II. 平衡二叉树](https://leetcode.cn/problems/ping-heng-er-cha-shu-lcof/)

输入一棵二叉树的根节点，判断该树是不是平衡二叉树。如果某二叉树中任意节点的左右子树的深度相差不超过1，那么它就是一棵平衡二叉树。

**示例 1:**

给定二叉树 `[3,9,20,null,null,15,7]`

```
    3
   / \
  9  20
    /  \
   15   7
```

返回 `true` 。

**示例 2:**

给定二叉树 `[1,2,2,3,3,null,null,4,4]`

```
       1
      / \
     2   2
    / \
   3   3
  / \
 4   4
```

返回 `false` 。

限制：

0 <= 树的结点个数 <= 10000

注意：本题与主站 110 题相同：https://leetcode-cn.com/problems/balanced-binary-tree/

## 方法一：后序遍历 + 剪枝 （从底至顶）

> 此方法为本题的最优解法，但剪枝的方法不易第一时间想到。

思路是对二叉树做后序遍历，从底至顶返回子树深度，若判定某子树不是平衡树则 “剪枝” ，直接向上返回。

算法流程：

**`recur(root)` 函数：**

- 返回值：
  - 当节点root 左 / 右子树的深度差 ≤1 ：则返回当前子树的深度，即节点 root 的左 / 右子树的深度最大值 +1 （ max(left, right) + 1 ）；
  - 当节点root 左 / 右子树的深度差 >2 ：则返回 -1 ，代表 此子树不是平衡树 。

- 终止条件：
  - 当 root 为空：说明越过叶节点，因此返回高度 0 ；
  - 当左（右）子树深度为 -1 ：代表此树的 左（右）子树 不是平衡树，因此剪枝，直接返回 −1 ；

isBalanced(root) 函数：

- 返回值： 若 recur(root) != -1 ，则说明此树平衡，返回 true ； 否则返回 false 。

时间复杂度 O(N)： N 为树的节点数；最差情况下，需要递归遍历树的所有节点。
空间复杂度 O(N)： 最差情况下（树退化为链表时），系统递归需要使用 O(N) 的栈空间。

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
    // 返回平衡树的最大深度，如果不是平衡树，返回 -1
    int dfs(TreeNode* node) {
        if (node == nullptr) return 0;
        int left = dfs(node->left);
        int right = dfs(node->right);
        // 如果左右子树都是平衡树，且子树的深度差小于等于 1，则该节点的树也是平衡树
        if (left != -1 && right != -1 && abs(left - right) <= 1) {
            // 返回当前平衡树的深度
            return max(left, right) + 1;
        }
        return -1;
    }
    bool isBalanced(TreeNode* root) {
        if (dfs(root) == -1) return false;
        return true;
    }
};
```

## 方法二：先序遍历 + 判断深度 （从顶至底）

思路是构造一个获取当前子树的深度的函数 depth(root) （即 面试题55 - I. 二叉树的深度 ），通过比较某子树的左右子树的深度差 abs(depth(root.left) - depth(root.right)) <= 1 是否成立，来判断某子树是否是二叉平衡树。若所有子树都平衡，则此树平衡。

- 时间复杂度：O(n^2)
- 空间复杂度：O(n)

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
    int height(TreeNode* node, int depth) {
        if (node == nullptr) return depth;
        return max(height(node->left, depth + 1), height(node->right, depth + 1));
    }

    bool isBalanced(TreeNode* root) {
        if (root == nullptr) return true;
        int left = height(root->left, 0);
        int right = height(root->right, 0);
        if (abs(left - right) <= 1 && isBalanced(root->left) && isBalanced(root->right)) return true;
        return false;
    }
};
```