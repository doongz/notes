题目：[剑指 Offer 09. 用两个栈实现队列](https://leetcode.cn/problems/yong-liang-ge-zhan-shi-xian-dui-lie-lcof/)

```c++
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

