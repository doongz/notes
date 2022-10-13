题目：[剑指 Offer II 023. 两个链表的第一个重合节点](https://leetcode.cn/problems/3u1WK4/)

```c++
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {
        ListNode *ptrA = headA;
        ListNode *ptrB = headB;
        if (ptrA == nullptr || ptrB == nullptr) return nullptr;

        while (ptrA != ptrB) {
            if (ptrA != nullptr) {
                ptrA = ptrA->next;
            } else {
                ptrA = headB;
            }

            if (ptrB != nullptr) {
                ptrB = ptrB->next;
            } else {
                ptrB = headA;
            }
        }
        // len(A) == len(B) 没有相交点，同时为nullptr时，跳出循环，不交叉遍历，ptrA为nullptr
        // len(A) == len(B) 有相交点，找到相交点，跳出循环，不交叉遍历，ptrA为相交点
        // len(A) != len(B) 没有相交点，交叉遍历, 最后同时为null时，跳出循环，ptrA为nullptr
        // len(A) ！= len(B) 有相交点，交叉遍历，找到相交点，跳出循环，ptrA为相交点
        return ptrA;
    }
};
```

