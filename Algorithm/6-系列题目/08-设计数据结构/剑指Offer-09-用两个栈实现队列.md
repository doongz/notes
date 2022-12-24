题目：[剑指 Offer 09. 用两个栈实现队列](https://leetcode.cn/problems/yong-liang-ge-zhan-shi-xian-dui-lie-lcof/)

用两个栈实现一个队列。队列的声明如下，请实现它的两个函数 appendTail 和 deleteHead ，分别完成在队列尾部插入整数和在队列头部删除整数的功能。(若队列中没有元素，deleteHead 操作返回 -1 )

```
示例 1：

输入：
["CQueue","appendTail","deleteHead","deleteHead","deleteHead"]
[[],[3],[],[],[]]
输出：[null,null,3,-1,-1]

示例 2：

输入：
["CQueue","deleteHead","appendTail","appendTail","deleteHead","deleteHead"]
[[],[],[5],[2],[],[]]
输出：[null,-1,null,null,5,2]
```

**提示：**

- `1 <= values <= 10000`
- 最多会对` appendTail、deleteHead `进行` 10000` 次调用



```cpp
class CQueue {
public:
    vector<int> addStack;
    vector<int> popStack;

    CQueue() {}

    void appendTail(int value) {
        addStack.push_back(value);
    }

    int deleteHead() {
        int ans;
        if (popStack.size() != 0) {
            ans = *popStack.rbegin();
        } else {
            if (addStack.size() == 0) return -1;
            while (addStack.size() != 0) {
                popStack.push_back(*addStack.rbegin());
                addStack.pop_back();
            }
            ans = *popStack.rbegin();
        }
        popStack.pop_back();
        return ans;
    }
};

/**
 * Your CQueue object will be instantiated and called as such:
 * CQueue* obj = new CQueue();
 * obj->appendTail(value);
 * int param_2 = obj->deleteHead();
 */
```

