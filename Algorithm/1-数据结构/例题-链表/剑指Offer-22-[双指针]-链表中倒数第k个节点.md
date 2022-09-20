题目：[剑指 Offer 22. 链表中倒数第k个节点](https://leetcode.cn/problems/lian-biao-zhong-dao-shu-di-kge-jie-dian-lcof/)

## 方法：双指针

右指针先走 k 个

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
    ListNode* getKthFromEnd(ListNode* head, int k) {
        ListNode* right = head;
        ListNode* left = head;

        while (k>1) {
            right = right->next;
            k--;
        }

        while (right->next) {
            right = right->next;
            left = left->next;
        }

        return left;
    }
};
```

