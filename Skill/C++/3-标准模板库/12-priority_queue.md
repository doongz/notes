# priority_queue

priority_queue 容器适配器模拟的也是队列这种存储结构，存储元素从一端进（称为队尾），从另一端出（称为队头），且每次只能访问 priority_queue 中位于队头的元素，容器内部按一定顺序排序，优先级最大的元素最先出队列

## 一、创建

priority_queue 容器适配器模板位于`<queue>`头文件中，默认是大根堆

```cpp
#include <array>
#include <iostream>
#include <queue>
using namespace std;

int main() {
    // 1 创建一个空的 priority_queue 容器适配器，第底层采用默认的 vector 容器
    priority_queue<int> q1;

    // 2 使用普通数组或其它容器中指定范围内的数据
    int val[]{4, 1, 3, 2};
    priority_queue<int> q2(val, val + 4);  // 4 3 2 1

    array<int, 4> arr{4, 1, 3, 2};
    priority_queue<int> q3(arr.begin(), arr.end());  // // 4 3 2 1

    // 3 手动指定 priority_queue 使用的底层容器以及排序规则
    int values[]{4, 1, 2, 3};
    priority_queue<int, deque<int>, greater<int> > q4(values, values + 4);
    // 1 2 3 4
    // 底层容器为 vector 会快一些
    priority_queue<int, vector<int>, greater<int> > q5(values, values + 4);

    while (!q4.empty()) {
        cout << q4.top() << " ";
        q4.pop();
    }

    return 0;
}
```

## 二、成员函数

| 成员函数                         | 功能                                                         |
| -------------------------------- | ------------------------------------------------------------ |
| **empty()**                      | **如果 priority_queue 为空的话，返回 true；反之，返回 false** |
| size()                           | 返回 priority_queue 中存储元素的个数。                       |
| **top()**                        | **返回 priority_queue 中第一个元素的引用形式**               |
| push(const T& obj)               | 根据既定的排序规则，将元素 obj 的副本存储到 priority_queue 中适当的位置。 |
| **push(T&& obj)**                | **根据既定的排序规则，将元素 obj 移动存储到 priority_queue 中适当的位置** |
| emplace(Args&&... args)          | Args&&... args 表示构造一个存储类型的元素所需要的数据（对于类对象来说，可能需要多个数据构造出一个对象）。此函数的功能是根据既定的排序规则，在容器适配器适当的位置直接生成该新元素。 |
| **pop()**                        | **移除 priority_queue 容器适配器中第一个元素**               |
| `swap(priority_queue<T>& other)` | 将两个 priority_queue 容器适配器中的元素进行互换，需要注意的是，进行互换的 2 个 priority_queue 容器适配器中存储的元素类型以及底层采用的基础容器类型，都必须相同。 |

```cpp
#include <iostream>
#include <queue>
using namespace std;
int main() {
    priority_queue<int> values;

    values.push(3);  //{3}
    values.push(1);  //{3,1}
    values.push(4);  //{4,1,3}
    values.push(2);  //{4,2,3,1}

    while (!values.empty()) {
        //输出第一个元素并移除。
        cout << values.top() << " ";
        values.pop();  //移除队头元素的同时，将剩余元素中优先级最大的移至队头
    }
    return 0;
}
```

