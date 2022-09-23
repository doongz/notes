题目：[剑指 Offer 36. 二叉搜索树与双向链表](https://leetcode.cn/problems/er-cha-sou-suo-shu-yu-shuang-xiang-lian-biao-lcof/)

```c++
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* left;
    Node* right;

    Node() {}

    Node(int _val) {
        val = _val;
        left = NULL;
        right = NULL;
    }

    Node(int _val, Node* _left, Node* _right) {
        val = _val;
        left = _left;
        right = _right;
    }
};
*/
class Solution {
public:
    vector<Node*> node_list;

    void dfs(Node* node) {
        if (node == nullptr) return;
        dfs(node->left);
        node_list.push_back(node);
        dfs(node->right);
    }
    Node* treeToDoublyList(Node* root) {
        if (root == nullptr) return root;
        dfs(root);

        int n = node_list.size();
        for (int i = 0; i < n - 1; i++) {
            node_list[i]->right = node_list[i + 1];
        }
        node_list[n - 1]->right = node_list[0];
        for (int i = n - 1; i > 0; i--) {
            node_list[i]->left = node_list[i - 1];
        }
        node_list[0]->left = node_list[n - 1];

        return node_list[0];
    }
};
```

原地算法

```c++
class Solution {
public:
    Node* treeToDoublyList(Node* root) {
        if (root == nullptr) return nullptr;
        dfs(root);
        head->left = pre;
        pre->right = head;
        return head;
    }

private:
    Node *pre, *head;
    void dfs(Node* cur) {
        if (cur == nullptr) return;
        dfs(cur->left);
        if (pre != nullptr) {
            pre->right = cur;
        } else {
            head = cur;
        }
        cur->left = pre;
        pre = cur;
        dfs(cur->right);
    }
};

```

