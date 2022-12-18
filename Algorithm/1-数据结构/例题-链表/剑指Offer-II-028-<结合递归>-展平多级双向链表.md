题目：[剑指 Offer II 028. 展平多级双向链表](https://leetcode.cn/problems/Qv1Da2/)

多级双向链表中，除了指向下一个节点和前一个节点指针之外，它还有一个子链表指针，可能指向单独的双向链表。这些子列表也可能会有一个或多个自己的子项，依此类推，生成多级数据结构，如下面的示例所示。

给定位于列表第一级的头节点，请扁平化列表，即将这样的多级双向链表展平成普通的双向链表，使所有结点出现在单级双链表中。

示例 1：

输入：head = [1,2,3,4,5,6,null,null,null,7,8,9,10,null,null,11,12]
输出：[1,2,3,7,8,11,12,9,10,4,5,6]
解释：

输入的多级列表如下图所示：

![](https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2018/10/12/multilevellinkedlist.png)

扁平化后的链表如下图：

![](https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2018/10/12/multilevellinkedlistflattened.png)

```
示例 2：

输入：head = [1,2,null,3]
输出：[1,3,2]
解释：

输入的多级列表如下图所示：

  1---2---NULL
  |
  3---NULL
示例 3：

输入：head = []
输出：[]
```

提示：

节点数目不超过 1000
1 <= Node.val <= 10^5


注意：本题与主站 430 题相同： https://leetcode-cn.com/problems/flatten-a-multilevel-doubly-linked-list/

## 自己写的

```c++
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* prev;
    Node* next;
    Node* child;
};
*/

class Solution {
public:
    Node* hair = new Node;
    Node* cur = hair;

    void dfs(Node* node) {
        if (node == nullptr) return;
        while (node != nullptr) {
            // cout << node->val << endl;
            // 需要现将当前 node 的下个节点存下来，因为dfs会导致node的next变化
            Node* temp = node->next;
            cur->next = node;
            node->prev = cur;
            cur = cur->next;
            if (node->child != nullptr) {
                dfs(node->child);
                node->child = nullptr;  // 注意要把child置为nullptr因为答案要的是双向链表
            }
            node = temp;
        }
    }

    Node* flatten(Node* head) {
        if (head == nullptr) return nullptr;
        dfs(head);
        Node* ans = hair->next;
        ans->prev = nullptr;  // 注意要把头节点的prev置为nullptr因为答案要的是双向链表
        return ans;
    }
};
```



## 破釜沉舟做法

```c++
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* prev;
    Node* next;
    Node* child;
};
*/

class Solution {
public:
    vector<Node*> node_list;
    void dfs(Node* node) {
        if (node == nullptr) return;
        while (node) {
            // cout << node->val << endl;
            node_list.push_back(node);
            if (node->child) {
                dfs(node->child);
                node->child = nullptr;
            }
            node = node->next;
        }
    }
    Node* flatten(Node* head) {
        if (head == nullptr) return nullptr;
        dfs(head);
        Node* hair = new Node();
        Node* cur = hair;
        for (Node *node : node_list) {
            cur->next = node;
            node->prev = cur;
            cur = cur->next;
        }
        Node* ans = hair->next;
        ans->prev = nullptr;
        return ans;
    }
};
```



## 别人的写法

```c++
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* prev;
    Node* next;
    Node* child;
};
*/

class Solution {
public:
    // 以cur开头的后续部分，返回展平后的尾结点last
    Node* dfs(Node* cur) {
        Node* last = cur;
        while (cur != nullptr) {
            Node* next = cur->next;
            if (cur->child != nullptr) {            // 有child则递归地处理child
                Node* childLast = dfs(cur->child);  // 展平处理的关键，总是先递归地处理child，得到当前链的最后一个结点
                cur->next = cur->child;             // 首次到此步说明已展平以cur.child为首的后续部分，则链接cur与child
                cur->child->prev = cur;
                cur->child = nullptr;
                if (next != nullptr) {  // 若有next，链接childLast与next
                    childLast->next = next;
                    next->prev = childLast;
                }
                last = childLast;
            } else {
                last = cur;  // 此行使得遍历到一层最后的cur == null时，能够返回最后一个结点
            }
            cur = next;  // 考察下一个结点
        }
        return last;
    }
    Node* flatten(Node* head) {
        dfs(head);
        return head;
    }
};
```

