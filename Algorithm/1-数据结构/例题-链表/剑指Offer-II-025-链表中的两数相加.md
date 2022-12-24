题目：[剑指 Offer II 025. 链表中的两数相加](https://leetcode.cn/problems/lMSNwu/)

给定两个 非空链表 l1和 l2 来代表两个非负整数。数字最高位位于链表开始位置。它们的每个节点只存储一位数字。将这两数相加会返回一个新的链表。

可以假设除了数字 0 之外，这两个数字都不会以零开头。

**示例1：**

![img](../../img/1626420025-fZfzMX-image.png)

```
输入：l1 = [7,2,4,3], l2 = [5,6,4]
输出：[7,8,0,7]
```

**示例2：**

```
输入：l1 = [2,4,3], l2 = [5,6,4]
输出：[8,0,7]
```

**示例3：**

```
输入：l1 = [0], l2 = [0]
输出：[0]
```

**提示：**

- 链表的长度范围为` [1, 100]`
- `0 <= node.val <= 9`
- 输入数据保证链表代表的数字无前导 0

进阶：如果输入链表不能修改该如何处理？换句话说，不能对列表中的节点进行翻转。

注意：本题与主站 445 题相同：https://leetcode-cn.com/problems/add-two-numbers-ii/

---

**update：统一回复下头插法的评论，不熟悉的可以用迭代法去做做 [206. 反转链表](https://leetcode-cn.com/problems/reverse-linked-list/)，需要链表逆序的时候就用头插法**。

用 stack 保存链表，再从 stack 中取出来，就是数字从低位到高位访问了。

```cpp
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

```cpp
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

