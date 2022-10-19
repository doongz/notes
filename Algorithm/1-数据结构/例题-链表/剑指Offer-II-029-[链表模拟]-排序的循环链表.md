题目：[剑指 Offer II 029. 排序的循环链表](https://leetcode.cn/problems/4ueAj6/)

题解：[【宫水三叶】常规链表模拟题](https://leetcode.cn/problems/4ueAj6/solution/by-ac_oier-kqv3/)

这是一道常规的链表模拟题。

为了方便，我们记 `insertVal` 为 `x`，记 `head` 为 `he`。

起始我们先将待插入的节点创建出来，记为 `t`，当 `he` 为空时，直接返回 `t` 即可。

由于我们需要返回原本的头结点，因此我们先使用变量 `ans` 对原始的 `he` 进行转存，随后复用 `he` 来充当游标进行遍历。

我们先对链表进行一次完成遍历，遍历过程中维护节点最值 `max` 和 `min`，由于链表是循环的，我们需要使用 `he.next != ans` 作为我们循环的结束条件，含义为回到链表开头。

此时根据最大值和最小值是否相等（即整段链表值是否一致）来进行分情况讨论：

- 若满足 `max = min`，此时目标节点 `t` 插入在哪个位置都满足条件，我们直接将其与 `ans` 关联即可；
- 若不满足 `max = min`，此时我们先对链表进行一次遍历，找到有序列表的结束点（结束点的定义为：当前节点值为最大值，下一节点值为最小值。即为有序链表分割位置的左端点），在根据「插入值 `x` 是否为新链表的最值」进行分情况讨论：
    - 若满足 `x >= max` 或 `x <= min` ，说明目标节点 `t` 插入分割位置即可；
    - 若不满足上述两条件，需要从分割位置出发，找到目标插入位置，即满足 `he.val <= x && x <= he.next.val` 的位置。

时间复杂度：O(n)

空间复杂度：O(1)

```c++
/*
// Definition for a Node.
class Node {
public:
    int val;
    Node* next;

    Node() {}

    Node(int _val) {
        val = _val;
        next = NULL;
    }

    Node(int _val, Node* _next) {
        val = _val;
        next = _next;
    }
};
*/

class Solution {
public:
    Node* insert(Node* head, int insertVal) {
        Node* insert_node = new Node(insertVal);
        if (head == nullptr) {
            insert_node->next = insert_node;
            return insert_node;
        }
        Node* cur = head;
        int max_val = INT_MIN;
        int min_val = INT_MAX;

        while (cur->next != head) {
            max_val = max(max_val, cur->val);
            min_val = min(min_val, cur->val);
            cur = cur->next;
        }  // 跳出循环时，cur 的值还没统计过
        max_val = max(max_val, cur->val);
        min_val = min(min_val, cur->val);
        // cout << max_val << " " << min_val << endl;

        if (max_val == min_val) {
            // 插哪里都可以
            Node* tmp = cur->next;
            cur->next = insert_node;
            insert_node->next = tmp;
        } else {
            // 对链表进行一次遍历，找到有序列表的结束点(当前节点值为最大值，下一节点值为最小值)
            while (true) {
                if (cur->val == max_val && cur->next->val == min_val) {
                    break;
                }
                cur = cur->next;
            }
            // cout << cur->val << " " << cur->next->val << endl;
            if (insertVal >= max_val || insertVal <= min_val) {
                Node* tmp = cur->next;
                cur->next = insert_node;
                insert_node->next = tmp;
            } else {
                while (true) {
                    if (cur->val <= insertVal && insertVal <= cur->next->val) {
                        Node* tmp = cur->next;
                        cur->next = insert_node;
                        insert_node->next = tmp;
                        break;
                    }
                    cur = cur->next;
                }
            }
        }

        return head;
    }
};
```

