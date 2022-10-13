题目：[剑指 Offer II 021. 删除链表的倒数第 n 个结点](https://leetcode.cn/problems/SLwz0R/)

```c++
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode* hair = new ListNode();
        hair->next = head;
        ListNode* right = hair;
        ListNode* left = hair;
        for (int i = 0; i < n; i++) {
            right = right->next;
        }
        while (right->next != nullptr) {
            right = right->next;
            left = left->next;
        }
        left->next = left->next->next;

        return hair->next;
    }
};
```

