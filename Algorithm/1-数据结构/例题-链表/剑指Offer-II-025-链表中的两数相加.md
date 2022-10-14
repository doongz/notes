题目：[剑指 Offer II 025. 链表中的两数相加](https://leetcode.cn/problems/lMSNwu/)

**update：统一回复下头插法的评论，不熟悉的可以用迭代法去做做 [206. 反转链表](https://leetcode-cn.com/problems/reverse-linked-list/)，需要链表逆序的时候就用头插法**。

用 stack 保存链表，再从 stack 中取出来，就是数字从低位到高位访问了。

```C++
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
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        stack<int> stk1;
        stack<int> stk2;
        while (l1) {
            stk1.push(l1->val);
            l1 = l1->next;
        }
        while (l2) {
            stk2.push(l2->val);
            l2 = l2->next;
        }
        int carry = 0;
        ListNode* head = nullptr;
        while (!stk1.empty() || !stk2.empty() || carry > 0) {
            int sum = carry;
            if (!stk1.empty()) {
                sum += stk1.top();
                stk1.pop();
            }
            if (!stk2.empty()) {
                sum += stk2.top();
                stk2.pop();
            }
            ListNode* node = new ListNode(sum % 10);
            node->next = head;
            head = node;
            carry = sum / 10;
        }
        return head;
    }
};
```



## 恢复成 arr 做法

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
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        vector<int> l1_arr;
        vector<int> l2_arr;
        while (l1) {
            l1_arr.push_back(l1->val);
            l1 = l1->next;
        }
        while (l2) {
            l2_arr.push_back(l2->val);
            l2 = l2->next;
        }

        int l1_sz = l1_arr.size();
        int l2_sz = l2_arr.size();
        reverse(l1_arr.begin(), l1_arr.end());
        reverse(l2_arr.begin(), l2_arr.end());
        int n;
        if (l1_sz < l2_sz) {
            for (int i = 0; i < l2_sz - l1_sz; i++) {
                l1_arr.push_back(0);
            }
            n = l2_sz;
        } else {
            for (int i = 0; i < l1_sz - l2_sz; i++) {
                l2_arr.push_back(0);
            }
            n = l1_sz;
        }
        l1_arr.push_back(0);  // 多扩充一位，为最顶层进位

        int pre = 0;  // 进位数
        for (int i = 0; i < n; i++) {
            int now = l1_arr[i] + l2_arr[i] + pre;
            if (now > 9) {
                pre = 1;
                l1_arr[i] = now - 10;
            } else {
                pre = 0;
                l1_arr[i] = now;
            }
        }
        int start;
        if (pre > 0) {
            l1_arr[n] = pre;
            start = n;
        } else {
            start = n - 1;
        }

        ListNode* head = new ListNode();
        ListNode* cur = head;
        for (int i = start; i >= 0; i--) {
            cur->val = l1_arr[i];
            if (i == 0) {
                cur->next = nullptr;
            } else {
                cur->next = new ListNode();
                cur = cur->next;
            }
        }
        return head;
    }
};
```

