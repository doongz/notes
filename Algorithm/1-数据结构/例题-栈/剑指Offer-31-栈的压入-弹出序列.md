题目：[剑指 Offer 31. 栈的压入、弹出序列](https://leetcode.cn/problems/zhan-de-ya-ru-dan-chu-xu-lie-lcof/)

输入两个整数序列，第一个序列表示栈的压入顺序，请判断第二个序列是否为该栈的弹出顺序。假设压入栈的所有数字均不相等。例如，序列 {1,2,3,4,5} 是某栈的压栈序列，序列 {4,5,3,2,1} 是该压栈序列对应的一个弹出序列，但 {4,3,5,1,2} 就不可能是该压栈序列的弹出序列。

```
示例 1：

输入：pushed = [1,2,3,4,5], popped = [4,5,3,2,1]
输出：true
解释：我们可以按以下顺序执行：
push(1), push(2), push(3), push(4), pop() -> 4,
push(5), pop() -> 5, pop() -> 3, pop() -> 2, pop() -> 1

示例 2：

输入：pushed = [1,2,3,4,5], popped = [4,3,5,1,2]
输出：false
解释：1 不能在 2 之前弹出。
```

提示：

0 <= pushed.length == popped.length <= 1000
0 <= pushed[i], popped[i] < 1000
pushed 是 popped 的排列。

注意：本题与主站 946 题相同：https://leetcode-cn.com/problems/validate-stack-sequences/

---

输入两个整数序列，第一个序列表示栈的压入顺序，请判断第二个序列是否为该栈的弹出顺序。假设压入栈的所有数字均不相等。例如，序列 {1,2,3,4,5} 是某栈的压栈序列，序列 {4,5,3,2,1} 是该压栈序列对应的一个弹出序列，但 {4,3,5,1,2} 就不可能是该压栈序列的弹出序列。

```
输入：pushed = [1,2,3,4,5], popped = [4,5,3,2,1]
输出：true
解释：我们可以按以下顺序执行：
push(1), push(2), push(3), push(4), pop() -> 4,
push(5), pop() -> 5, pop() -> 3, pop() -> 2, pop() -> 1

输入：pushed = [1,2,3,4,5], popped = [4,3,5,1,2]
输出：false
解释：1 不能在 2 之前弹出。
```

按照 popped 中的顺序进行检查

```
输入：pushed = [1,2,3,4,5], popped = [4,5,3,2,1]

1、popped[0]为4，pushed按顺序入栈，直到pushed[3]入栈的值为4，此时栈内的值为 [1,2,3,4]，把 4 pop 掉
2、popped[1]为5，检查栈顶的值是否为5，此时是3不为5，
   从pushed[4]入栈，直到pushed[4]入栈的值为5，此时栈内的值为 [1,2,3,5]，把 5 pop 掉
3、popped[2]为3，检查栈顶的值是否为3，此时是3，把 3 pop 掉
4、popped[3]为2，检查栈顶的值是否为2，此时是2，把 2 pop 掉
5、popped[4]为1，检查栈顶的值是否为1，此时是1，把 1 pop 掉

返回 True
```

那什么时候返回 False 呢？

**当栈顶的值不为 popped[j]，且把 pushed[i] 后面的值都加入栈后，都没有等于 popped[j] 的，返回 False**

**此方法正确性的保障是：假设压入栈的所有数字均不相等**

```cpp
class Solution {
public:
    bool validateStackSequences(vector<int>& pushed, vector<int>& popped) {
        vector<int> st;
        int push_sz = pushed.size();  // i
        int pop_sz = pushed.size();   // j
        int i = 0;
        int j = 0;

        while (j < pop_sz) {
            // 先检查 pop_sz[j] 和栈顶是否一样
            if (!st.empty() && popped[j] == *st.rbegin()) {
                st.pop_back();  // 移除栈顶
                j++;            // 检查下一个 popped
                continue;
            }

            // 和栈顶不一样，不断的往栈里加，直到一样或 pushed 越界
            while (i < push_sz && popped[j] != pushed[i]) {
                st.push_back(pushed[i]);
                i++;
            }
            // 此时可能 i == push_sz，越界直接返回 false
            if (i == push_sz) return false;
            // 也可能 popped[j] == push_sz[i]，添加进去再移除，本质上什么都不用做

            // 继续检查 popped 和 push_sz 的下一位
            j++;
            i++;
        }
        return true;
    }
};
```

另一种解法：

```python
class Solution:
    def validateStackSequences(self, pushed: List[int], popped: List[int]) -> bool:
        stack, i = [], 0
        for num in pushed:
            stack.append(num) # num 入栈
            while stack and stack[-1] == popped[i]: # 循环判断与出栈
                stack.pop()
                i += 1
        return not stack
```

