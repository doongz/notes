# 双端队列容器 deque

deque 是 double-ended queue 的缩写，又称双端队列容器，当需要向序列两端频繁的添加或删除元素时，应首选 deque 容器。

- deque 容器擅长在序列尾部添加或删除元素，时间复杂度为`O(1)`，不擅长在序列中间添加或删除元素。
- deque 还擅长在序列头部添加或删除元素，时间复杂度也为常数阶`O(1)`
- deque 容器也可以根据需要修改自身的容量和大小。
- eque 容器中存储元素并不能保证所有元素都存储到连续的内存空间中

## 一、创建deque容器

```cpp
#include <array>
#include <deque>
#include <iostream>
using namespace std;

int main() {
    // 1、创建一个没有任何元素的空 deque 容器
    deque<int> q1;  // {}

    // 2、创建一个具有 n 个元素的 deque 容器，其中每个元素都采用对应类型的默认值
    deque<int> q2(5);  // {0 0 0 0 0}

    // 3、创建一个具有 n 个元素的 deque 容器，并为每个元素都指定初始值
    deque<int> q3(5, 1);  // {1 1 1 1 1}

    // 4、拷贝到一个新的 deque 容器
    deque<int> q4(q3);  // {1 1 1 1 1}

    // 5、拷贝其他类型容器中指定区域内的元素
    array<int, 5> arr{11, 12, 13, 14, 15};
    deque<int> d(arr.begin() + 2, arr.end());  // {13,14,15}

    return 0;
}
```

## 二、成员函数

| 函数成员         | 函数功能                                                     |
| ---------------- | ------------------------------------------------------------ |
| begin()          | 返回指向容器中第一个元素的迭代器。                           |
| end()            | 返回指向容器最后一个元素所在位置后一个位置的迭代器，通常和 begin() 结合使用。 |
| rbegin()         | 返回指向最后一个元素的迭代器。                               |
| rend()           | 返回指向第一个元素所在位置前一个位置的迭代器。               |
| cbegin()         | 和 begin() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。 |
| cend()           | 和 end() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。 |
| crbegin()        | 和 rbegin() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。 |
| crend()          | 和 rend() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。 |
| size()           | 返回实际元素个数。                                           |
| max_size()       | 返回容器所能容纳元素个数的最大值。这通常是一个很大的值，一般是 232-1，我们很少会用到这个函数。 |
| resize()         | 改变实际元素的个数。                                         |
| empty()          | 判断容器中是否有元素，若无元素，则返回 true；反之，返回 false。 |
| shrink _to_fit() | 将内存减少到等于当前元素实际所使用的大小。                   |
| at()             | 使用经过边界检查的索引访问元素。                             |
| **front()**      | **返回第一个元素的引用。**                                   |
| back()           | 返回最后一个元素的引用。                                     |
| assign()         | 用新元素替换原有内容。                                       |
| **push_back()**  | **在序列的尾部添加一个元素**                                 |
| **push_front()** | **在序列的头部添加一个元素**                                 |
| **pop_back()**   | **移除容器尾部的元素**                                       |
| **pop_front()**  | **移除容器头部的元素**                                       |
| insert()         | 在指定的位置插入一个或多个元素。                             |
| erase()          | 移除一个元素或一段元素。                                     |
| clear()          | 移出所有的元素，容器大小变为 0。                             |
| swap()           | 交换两个容器的所有元素。                                     |
| emplace()        | 在指定的位置直接生成一个元素。                               |
| emplace_front()  | 在容器头部生成一个元素。和 push_front() 的区别是，该函数直接在容器头部构造元素，省去了复制移动元素的过程。 |
| emplace_back()   | 在容器尾部生成一个元素。和 push_back() 的区别是，该函数直接在容器尾部构造元素，省去了复制移动元素的过程。 |

## 三、随机访问迭代器

begin() 和 end() 分别用于指向「首元素」和「尾元素+1」 的位置

迭代器的功能是遍历容器，在遍历的同时可以访问（甚至修改）容器中的元素，但迭代器不能用来初始化空的 deque 容器

除此之外，当向 deque 容器添加元素时，deque 容器会申请更多的内存空间，同时其包含的所有元素可能会被复制或移动到新的内存地址（原来占用的内存会释放），这会导致之前创建的迭代器失效。所以使用前一定要重新指定迭代器

```cpp
#include <deque>
#include <iostream>
using namespace std;

int main() {
    deque<int> q{1, 2, 3, 4, 5};

    for (auto i = q.begin(); i < q.end(); i++) {
        cout << *i << " ";
    }
    cout << endl;  // 1 2 3 4 5

    for (auto i = q.rbegin(); i < q.rend(); i++) {
        cout << *i << " ";
    }
    cout << endl;  // 5 4 3 2 1

    return 0;
}
```

## 四、访问元素

`容器名[n]`的这种方式，不仅可以访问容器中的元素，还可以对其进行修改。但下标越界，不会报错

at() 成员函数具备上述的功能，而且下标越界会报错，但是性能低

 front() 和 back() 成员函数，它们分别返回 vector 容器中第一个和最后一个元素的引用，通过利用它们的返回值，可以访问和修改容器中的首尾元素

```cpp
deque<int> q{1, 2, 3, 4, 5};

cout << q[1] << endl;  // 2
q[1] = 9;
cout << q[1] << endl;  // 9

cout << q.at(4) << endl;  // 5
cout << q[100] << endl;   // 0 不报错
// cout << q.at(100) << endl;  // 报错

q.front() = 10;
cout << q.front() << endl;  // 10
cout << q.back() << endl;   // 5
```

begin() end() 遍历 deque 容器中指定区域元素

```cpp
deque<int> q{1, 2, 3, 4, 5};

for (auto i = q.begin() + 1; i < q.end() - 1; i++) {
    cout << *i << " ";
}
cout << endl;  // 2 3 4

auto first = q.begin() + 1;
auto end = q.end() - 1;
while (first < end) {
    cout << *first << " ";
    first++;
}
cout << endl;  // 2 3 4
```

## 五、添加和删除元素

头部、尾部处理

```cpp
deque<int> q{1, 2, 3};
// 尾部添加
q.push_back(9);  // 1 2 3 9

// 尾部移除
q.pop_back();  // 1 2 3

// 头部添加
q.push_front(8);  // 8 1 2 3

// 头部移除
q.pop_front();  // 1 2 3

// 容器中尾、头部直接生成数据
q.emplace_back(9);   // 1 2 3 9
q.emplace_front(8);  // 8 1 2 3 9

// 在指定位置添加
q.emplace(q.begin() + 1, 7);  // 8 7 1 2 3 9

// erase()可以接受一个迭代器表示要删除元素所在位置
//也可以接受 2 个迭代器，表示要删除元素所在的区域。
q.erase(q.begin());           // 7 1 2 3 9
q.erase(q.begin(), q.end());  //{}，等同于 q.clear()
```

insert() 函数具体用法

```cpp
std::deque<int> q{1, 2};

q.insert(q.begin() + 1, 3);  // 1 3 2
q.insert(q.end(), 2, 5);     // 1 3 2 5 5

std::array<int, 3> t{7, 8, 9};
q.insert(q.end(), t.begin(), t.end());  // 1 3 2 5 5 7 8 9
q.insert(q.end(), {10, 11});            // 1 3 2 5 5 7 8 9 10 11
```

emplace系列函数 性能更优

