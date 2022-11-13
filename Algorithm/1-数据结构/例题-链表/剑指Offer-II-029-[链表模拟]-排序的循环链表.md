题目：[剑指 Offer II 029. 排序的循环链表](https://leetcode.cn/problems/4ueAj6/)

题解：[【宫水三叶】常规链表模拟题](https://leetcode.cn/problems/4ueAj6/solution/by-ac_oier-kqv3/)

给定循环单调非递减列表中的一个点，写一个函数向这个列表中插入一个新元素 insertVal ，使这个列表仍然是循环升序的。

给定的可以是这个列表中任意一个顶点的指针，并不一定是这个列表中最小元素的指针。

如果有多个满足条件的插入位置，可以选择任意一个位置插入新的值，插入后整个列表仍然保持有序。

如果列表为空（给定的节点是 null），需要创建一个循环有序列表并返回这个节点。否则。请返回原先给定的节点。

**示例 1：**

![img](https://assets.leetcode.com/uploads/2019/01/19/example_1_before_65p.jpg)

```
输入：head = [3,4,1], insertVal = 2
输出：[3,4,1,2]
解释：在上图中，有一个包含三个元素的循环有序列表，你获得值为 3 的节点的指针，我们需要向表中插入元素 2 。新插入的节点应该在 1 和 3 之间，插入之后，整个列表如上图所示，最后返回节点 3 。
```

```
示例 2：

输入：head = [], insertVal = 1
输出：[1]
解释：列表为空（给定的节点是 null），创建一个循环有序列表并返回这个节点。

示例 3：

输入：head = [1], insertVal = 0
输出：[1,0]
```

提示：

0 <= Number of Nodes <= 5 * 10^4
-10^6 <= Node.val <= 10^6
-10^6 <= insertVal <= 10^6


注意：本题与主站 708 题相同： https://leetcode-cn.com/problems/insert-into-a-sorted-circular-linked-list/

---

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

