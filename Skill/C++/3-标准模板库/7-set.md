# set 容器

使用 set 容器存储的各个键值对，**键 key 和值 value 必须相等**

{<'a', 1>, <'b', 2>, <'c', 3>}
{<'a', 'a'>, <'b', 'b'>, <'c', 'c'>}

对于 set 容器来说，只能存储第 2 组键值对。基于 set 容器的这种特性，**只需要为其提供各键值对中的 value 值**

set 容器会自行根据键的大小对存储的键值对进行排序。**默认升序**

**常用 multiset，**因为可以存相同的值

## 一、创建

```c++
#include <iostream>
#include <set>
#include <string>
using namespace std;

int main() {
    // 1 调用默认构造函数，创建空的 set 容器
    set<string> s1;

    // 2 创建同时，对其进行初始化
    set<string> s2{"a", "b", "b", "c"};  // a b c

    // 3 拷贝（复制）构造函数
    set<string> s3(s2);  // a b c

    // 4 部分元素
    set<string> s4(++s2.begin(), s2.end());  // b c

    // 5 排序，指定比较算法
    set<string, greater<string>> s5{"b", "a", "b", "c"};  // c b a

    for (auto it = s5.begin(); it != s5.end(); it++) {
        cout << *it << " ";
    }
    return 0;
}
```

## 二、成员方法

| 成员方法         | 功能                                                         |
| ---------------- | ------------------------------------------------------------ |
| **begin()**      | **返回指向容器中第一个（注意，是已排好序的第一个）元素的双向迭代器。如果 set 容器用 const 限定，则该方法返回的是 const 类型的双向迭代器** |
| **end()**        | **返回指向容器中「最后」一个键值对「之后」位置的正向迭代器** |
| rbegin()         | 返回指向最后一个（注意，是已排好序的最后一个）元素的反向双向迭代器。如果 set 容器用 const 限定，则该方法返回的是 const 类型的反向双向迭代器。 |
| rend()           | 返回指向第一个（注意，是已排好序的第一个）元素所在位置前一个位置的反向双向迭代器。如果 set 容器用 const 限定，则该方法返回的是 const 类型的反向双向迭代器。 |
| cbegin()         | 和 begin() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改容器内存储的元素值。 |
| cend()           | 和 end() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改容器内存储的元素值。 |
| crbegin()        | 和 rbegin() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改容器内存储的元素值。 |
| crend()          | 和 rend() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改容器内存储的元素值。 |
| find(val)        | 在 set 容器中查找值为 val 的元素，如果成功找到，则返回指向该元素的双向迭代器；反之，则返回和 end() 方法一样的迭代器。另外，如果 set 容器用 const 限定，则该方法返回的是 const 类型的双向迭代器。 |
| lower_bound(val) | 返回一个指向当前 set 容器中第一个大于或等于 val 的元素的双向迭代器。如果 set 容器用 const 限定，则该方法返回的是 const 类型的双向迭代器。 |
| upper_bound(val) | 返回一个指向当前 set 容器中第一个大于 val 的元素的迭代器。如果 set 容器用 const 限定，则该方法返回的是 const 类型的双向迭代器。 |
| equal_range(val) | 该方法返回一个 pair 对象（包含 2 个双向迭代器），其中 pair.first 和 lower_bound() 方法的返回值等价，pair.second 和 upper_bound() 方法的返回值等价。也就是说，该方法将返回一个范围，该范围中包含的值为 val 的元素（set 容器中各个元素是唯一的，因此该范围最多包含一个元素）。 |
| **empty()**      | **若容器为空，则返回 true；否则 false**                      |
| **size()**       | **返回当前 set 容器中存有元素的个数**                        |
| max_size()       | 返回 set 容器所能容纳元素的最大个数，不同的操作系统，其返回值亦不相同。 |
| **insert()**     | **向 set 容器中插入元素**                                    |
| **erase()**      | **删除 set 容器中存储的元素，multiset 会把与指定值相同的都删了** |
| swap()           | 交换 2 个 set 容器中存储的所有元素。这意味着，操作的 2 个 set 容器的类型必须相同。 |
| clear()          | 清空 set 容器中所有的元素，即令 set 容器的 size() 为 0。     |
| emplace()        | 在当前 set 容器中的指定位置直接构造新元素。其效果和 insert() 一样，但效率更高。 |
| emplace_hint()   | 在本质上和 emplace() 在 set 容器中构造新元素的方式是一样的，不同之处在于，使用者必须为该方法提供一个指示新元素生成位置的迭代器，并作为该方法的第一个参数。 |
| count(val)       | 在当前 set 容器中，查找值为 val 的元素的个数，并返回。注意，由于 set 容器中各元素的值是唯一的，因此该函数的返回值最大为 1。 |

## 三、双向迭代器

访问 set 容器中存储的元素，只能借助 set 容器的迭代器

STL 标准库为 set 容器配置的迭代器类型为双向迭代器。这意味着，假设 p 为此类型的迭代器，则其只能进行 ++p、p++、--p、p--、*p 操作，并且 2 个双向迭代器之间做比较，也只能使用 == 或者 != 运算符。

```c++
set<string> s{"a", "b", "b", "c"};

for (auto it = s.begin(); it != s.end(); it++) {
    cout << *it << " ";
}  // a b c
for (auto it = s.rbegin(); it != s.rend(); it++) {
    cout << *it << " ";
}  // c b a
```

只想遍历 set 容器中指定区域内的部分数据，则可以借助 find()、lower_bound() 以及 upper_bound() 实现

```c++
set<string> s{"a", "b", "b", "c"};
auto f = s.find("b");
auto first = s.lower_bound("b");
auto end = s.upper_bound("b");

cout << *f << endl;      // b
cout << *first << endl;  // b
cout << *end << endl;    // c
```

## 四、插入元素

insert() 方法，返回的都是 pair 类型的值，其包含 2 个数据，一个迭代器和一个 bool 值：

- 当向 set 容器添加元素成功时，该迭代器指向 set 容器新添加的元素，bool 类型的值为 true；
- 如果添加失败，即证明原 set 容器中已存有相同的元素，此时返回的迭代器就指向容器中相同的此元素，同时 bool 类型的值为 false。

```c++
set<string> s{"a", "b", "b", "c"};
auto res1 = s.insert("d");
auto res2 = s.insert("b");

cout << *(res1.first) << " " << res1.second << endl; // d 1
cout << *(res2.first) << " " << res2.second << endl; // b 0
```

emplace() 和 emplace_hint() 是 C++11 标准加入到 set 类模板中的，相比具有同样功能的 insert() 方法，完成同样的任务，emplace() 和 emplace_hint() 的效率会更高。

## 五、删除元素

删除 set 容器存储的元素，可以选择用 erase() 或者 clear() 成员方法

```c++
set<string> s{"a", "b", "b", "c", "d", "e"};
// a b c d e

s.erase("b");                   // a c d e
s.erase(s.begin());             // c d e
s.erase(++s.begin(), s.end());  // 
```

## 六、multiset（常用）

multiset 容器和 set 容器唯一的差别在于，multiset 容器允许存储多个值相同的元素，而 set 容器中只能存储互不相同的元素

```c++
multiset<string> s1;
multiset<string> s2{"a", "c", "b", "b"};      // a b b c
multiset<string> s3(s2);                      // a b b c
multiset<string> s4(++s2.begin(), s2.end());  // b b c
```

- 用 `s1.erase("b")` 这种方式删除元素时，会将所有相同的元素删除
- 先用 `s2.lower_bound("b")` 找到第一个与指定值相等的迭代器，转为 `const`，然后删除 `s2.erase(it)`

```c++
#include <iostream>
#include <set>
#include <string>
using namespace std;

int main() {
    multiset<string> s1{"a", "c", "b", "b"};  // a b b c
    s1.erase("b");
    for (auto it = s1.begin(); it != s1.end(); it++) {
        cout << *it << " ";
    }
    cout << endl;  // a c

    multiset<string> s2{"a", "c", "b", "b"};  // a b b c
    const auto it = s2.lower_bound("b");      // 找到第一个与指定值相等的迭代器
    s2.erase(it);                             // 注意这个仅接受常数
    for (auto itt = s2.begin(); itt != s2.end(); itt++) {
        cout << *itt << " ";
    }  // a b c
    return 0;
}
```

