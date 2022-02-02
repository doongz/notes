# unordered_set

unordered_set 容器具有以下几个特性：

1. 不再以键值对的形式存储数据，而是直接存储数据的值；
2. 容器内部存储的各个元素的值都互不相等，且不能被修改。
3. 不会对内部存储的数据进行排序

对于 unordered_set 容器不以键值对的形式存储数据，也可以这样认为，即 unordered_set 存储的都是键和值相等的键值对，为了节省存储空间，该类容器在实际存储时选择只存储每个键值对的值。

## 一、创建

```c++
#include <iostream>
#include <string>
#include <vector>
#include <unordered_set>
using namespace std;

int main() {
    // 1 通过调用 unordered_set 模板类的默认构造函数
    unordered_set<string> us1;

    // 2 创建的同时初始化
    unordered_set<string> us2{"a", "b", "c"};

    // 3 复制（拷贝）构造函数
    unordered_set<string> us3(us2);  // a c b

    // 4 部分选择
    unordered_set<string> us4(++us2.begin(), us2.end());  // a c
  
    // 5 不同类型的容器转换
    vector<int> vec = {1, 2, 3, 2};
    unordered_set<int> us5(vec.begin(), vec.end()); // 3 2 1

    for (auto it = us4.begin(); it != us4.end(); it++) {
        cout << *it << " ";
    }  // a c b
    return 0;
}

```

## 二、成员方法

| 成员方法           | 功能                                                         |
| ------------------ | ------------------------------------------------------------ |
| **begin()**        | **返回指向容器中第一个元素的正向迭代器。**                   |
| **end();**         | **返回指向容器中最后一个元素之后位置的正向迭代器。**         |
| cbegin()           | 和 begin() 功能相同，只不过其返回的是 const 类型的正向迭代器。 |
| cend()             | 和 end() 功能相同，只不过其返回的是 const 类型的正向迭代器。 |
| empty()            | 若容器为空，则返回 true；否则 false。                        |
| **size()**         | **返回当前容器中存有元素的个数。**                           |
| max_size()         | 返回容器所能容纳元素的最大个数，不同的操作系统，其返回值亦不相同。 |
| find(key)          | 查找以值为 key 的元素，如果找到，则返回一个指向该元素的正向迭代器；反之，则返回一个指向容器中最后一个元素之后位置的迭代器（如果 end() 方法返回的迭代器）。 |
| **count(key)**     | **在容器中查找值为 key 的元素的个数。用来检测在不在里面**    |
| equal_range(key)   | 返回一个 pair 对象，其包含 2 个迭代器，用于表明当前容器中值为 key 的元素所在的范围。 |
| emplace()          | 向容器中添加新元素，效率比 insert() 方法高。                 |
| emplace_hint()     | 向容器中添加新元素，效率比 insert() 方法高。                 |
| **insert()**       | **向容器中添加新元素。**                                     |
| **erase()**        | **删除指定元素。**                                           |
| clear()            | 清空容器，即删除容器中存储的所有元素。                       |
| swap()             | 交换 2 个 unordered_map 容器存储的元素，前提是必须保证这 2 个容器的类型完全相等。 |
| bucket_count()     | 返回当前容器底层存储元素时，使用桶（一个线性链表代表一个桶）的数量。 |
| max_bucket_count() | 返回当前系统中，unordered_map 容器底层最多可以使用多少桶。   |
| bucket_size(n)     | 返回第 n 个桶中存储元素的数量。                              |
| bucket(key)        | 返回值为 key 的元素所在桶的编号。                            |
| load_factor()      | 返回 unordered_map 容器中当前的负载因子。负载因子，指的是的当前容器中存储元素的数量（size()）和使用桶数（bucket_count()）的比值，即 load_factor() = size() / bucket_count()。 |
| max_load_factor()  | 返回或者设置当前 unordered_map 容器的负载因子。              |
| rehash(n)          | 将当前容器底层使用桶的数量设置为 n。                         |
| reserve()          | 将存储桶的数量（也就是 bucket_count() 方法的返回值）设置为至少容纳count个元（不超过最大负载因子）所需的数量，并重新整理容器。 |
| hash_function()    | 返回当前容器使用的哈希函数对象。                             |

```c++
#include <iostream>
#include <string>
#include <unordered_set>
using namespace std;

int main() {
    unordered_set<string> us{"a", "b", "c"};
    us.insert("a");  // b c a

    us.erase("b");  // c a

    for (auto it = us.begin(); it != us.end(); it++) {
        cout << *it << " ";
    }
    return 0;
}

```

## 三、unordered_multiset

unordered_multiset 除了能存储相同值的元素外，它和 unordered_set 容器完全相同。

unordered_multiset 容器可以同时存储多个值相同的元素，且这些元素会存储到哈希表中同一个桶（本质就是链表）上。

```c++
unordered_multiset<string> ums{"b", "a", "b", "c"};

for (auto it = ums.begin(); it != ums.end(); it++) {
    cout << *it << " ";
}  // a c b b
```

