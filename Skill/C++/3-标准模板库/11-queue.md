# queue

queue 容器适配器有 2 个开口，其中一个开口专门用来输入数据，另一个专门用来输出数据

最先进入 queue 的元素，也可以最先从 queue 中出来，即用此容器适配器存储数据具有“先进先出（简称 "FIFO" ）”的特点，因此 queue 又称为队列适配器

![](../doc/queue.png)

## 一、创建

```c++
#include <deque>
#include <iostream>
#include <list>
#include <queue>
using namespace std;

int main() {
    // 1 创建一个空的 queue 容器适配器，其底层使用的基础容器选择默认的 deque 容器
    queue<int> q1;

    // 2 当手动指定 queue 容器适配器底层采用的 list 基础容器类型
    queue<int, list<int> > q2;

    // 3 创建并初始化
    deque<int> values{1, 2, 3};
    queue<int> q3(values);

    // 4 复制
    queue<int> q4(q3);

    return 0;
}

```

## 二、成员函数

| 成员函数                      | 功能                                                         |
| ----------------------------- | ------------------------------------------------------------ |
| **empty()**                   | **如果 queue 中没有元素的话，返回 true**                     |
| **size()**                    | **返回 queue 中元素的个数**                                  |
| **front()**                   | **返回 queue 中第一个元素的引用。如果 queue 是常量，就返回一个常引用；如果 queue 为空，返回值是未定义的** |
| back()                        | 返回 queue 中最后一个元素的引用。如果 queue 是常量，就返回一个常引用；如果 queue 为空，返回值是未定义的。 |
| **push(const T& obj)**        | **在 queue 的尾部添加一个元素的副本。这是通过调用底层容器的成员函数 push_back() 来完成的** |
| emplace()                     | 在 queue 的尾部直接添加一个元素。                            |
| push(T&& obj)                 | 以移动的方式在 queue 的尾部添加元素。这是通过调用底层容器的具有右值引用参数的成员函数 push_back() 来完成的。 |
| **pop()**                     | **删除 queue 中的第一个元素**                                |
| `swap(queue<T> &other_queue)` | 将两个 queue 容器适配器中的元素进行互换，需要注意的是，进行互换的 2 个 queue 容器适配器中存储的元素类型以及底层采用的基础容器类型，都必须相同。 |

```c++
#include <deque>
#include <iostream>
#include <queue>
using namespace std;

int main() {
    deque<int> values{1, 2, 3};
    queue<int> q(values);

    cout << q.size() << endl;  // 3

    while (!q.empty()) {
        cout << q.front() << " ";
        q.pop();
    }
    // 1 2 3

    return 0;
}
```

