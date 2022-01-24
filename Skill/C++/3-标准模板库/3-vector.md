# 向量 vector

vector 常被称为向量容器，因为该容器在尾部插入或删除元素的时间复杂度为`O(1)`；在容器头部或者中部插入或删除元素的时间复杂度为线性阶`O(n)`（移动元素需要耗费时间）

不同之处在于，array 实现的是静态数组（容量固定的数组），而 vector 实现的是一个动态数组，即可以进行元素的插入和删除，在此过程中，vector 会动态调整所占用的内存空间，整个过程无需人工干预。

## 一、创建 vector

```c++
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> vec1;
    vector<int> vec2{1, 2, 3, 4, 5};  // 1 2 3 4 5
    vector<int> vec3(5);              // 0 0 0 0 0
    vector<int> vec4(5, 1);           // 1 1 1 1 1
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
| max_size()       | 返回元素个数的最大值。这通常是一个很大的值，一般是 232-1，所以我们很少会用到这个函数。 |
| resize()         | 改变实际元素的个数。                                         |
| capacity()       | 返回当前容量。                                               |
| empty()          | 判断容器中是否有元素，若无元素，则返回 true；反之，返回 false。 |
| reserve()        | 增加容器的容量。                                             |
| shrink _to_fit() | 将内存减少到等于当前元素实际所使用的大小。                   |
| operator[ ]      | 重载了 [ ] 运算符，可以向访问数组中元素那样，通过下标即可访问甚至修改 vector 容器中的元素。 |
| at()             | 使用经过边界检查的索引访问元素。                             |
| front()          | 返回第一个元素的引用。                                       |
| back()           | 返回最后一个元素的引用。                                     |
| data()           | 返回指向容器中第一个元素的指针。                             |
| assign()         | 用新元素替换原有内容。                                       |
| push_back()      | 在序列的尾部添加一个元素。                                   |
| pop_back()       | 移出序列尾部的元素。                                         |
| insert()         | 在指定的位置插入一个或多个元素。                             |
| erase()          | 移出一个元素或一段元素。                                     |
| clear()          | 移出所有的元素，容器大小变为 0。                             |
| swap()           | 交换两个容器的所有元素。                                     |
| emplace()        | 在指定的位置直接生成一个元素。                               |
| emplace_back()   | 在序列尾部生成一个元素。                                     |

```c++
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<char> value;
    value.push_back('S');
    value.push_back('T');
    value.push_back('L');
    printf("size: %d\n", value.size());  // size: 3

    for (auto i = value.begin(); i < value.end(); i++) {
        cout << *i << " ";
    }
    cout << endl;  // S T L

    value.insert(value.begin(), 'C');
    cout << "first: " << value.at(0) << endl;  // first: C
    return 0;
}
```

## 三、随机访问迭代器

 begin() 和 end() 成员函数，它们分别用于指向「首元素」和「尾元素+1」 的位置

vector 模板类中还提供了 rbegin() 和 rend() 成员函数，分别表示指向最后一个元素和第一个元素前一个位置的随机访问迭代器，又称它们为反向迭代器，在使用反向迭代器进行 ++ 或 -- 运算时，++ 指的是迭代器向左移动一位，-- 指的是迭代器向右移动一位，即这两个运算符的功能也“互换”了

cbegin()/cend() 成员函数返回的是 const 类型的正向迭代器，这就意味着，由 cbegin() 和 cend() 成员函数返回的迭代器，可以用来遍历容器内的元素，但是不能对所存储的元素进行修改。

```c++
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> values{1, 2, 3, 4, 5};

    auto first = values.begin();
    auto end = values.end();
    while (first != end) {
        cout << *first << " ";
        ++first;
    }
    cout << endl;  // 1 2 3 4 5

    for (auto i = values.begin(); i != values.end(); i++) {
        cout << *i << " ";
    }
    cout << endl;  // 1 2 3 4 5

    for (auto i = values.rbegin(); i != values.rend(); i++) {
        cout << *i << " ";
    }
    cout << endl;  // 5 4 3 2 1

    return 0;
}
```

**vector 容器随着存储元素的增加自行申请更多的存储空间会引起一些问题，需要注意**

1）初始化空的 vector 容器时，不能使用迭代器

2）vector 容器在申请更多内存的同时，容器中的所有元素可能会被复制或移动到新的内存地址，这会导致之前创建的迭代器失效，所以之前创建的迭代器重新初始化一遍。

```c++
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> values{1, 2, 3};
    auto first = values.begin();
    auto end = values.end();

    // 查看 vector 第一个元素的地址
    cout << values.data() << endl;  // 0x60000000c000

    values.reserve(20);             // 增加 values 的容量
    cout << values.data() << endl;  // 0x600002104000

    // 如果不重新获取首元素的地址，下面的输出是混乱的 -559054832488132043
    // first = values.begin();
    // end = values.end();
    while (first != end) {
        cout << *first;
        ++first;
    }
    return 0;
}
```

## 四、访问元素

### 1、访问单个元素

- values[0] 性能好，不做越界判断

- values.at(4)  性能略差，但做越界判断

- front() 和 back() 成员函数，分别返回 vector 容器中第一个和最后一个元素的「引用」，通过利用这 2 个函数返回的引用，可以访问（甚至修改）容器中的首尾元素
- data() 成员函数，该函数的功能是返回指向容器中首个元素的「指针」

```c++
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> values{1, 2, 3, 4, 5};

    cout << values[0] << endl;                                  // 1
    values[0] = values[1] + values[2] + values[3] + values[4];  // 修改
    cout << values[0] << endl;                                  // 14

    cout << values.at(4) << endl;  // 如果越界会报错 5

    values.front() = 7;
    cout << values.front() << endl;  // 7
    cout << values.back() << endl;   // 5

    cout << *values.data();  // 7
    return 0;
}
```

### 2、访问多个元素

```c++
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> values{1, 2, 3, 4, 5};

    for (int i = 0; i < values.size(); i++) {
        cout << values[i] << " ";
    }
    cout << endl;  // 1 2 3 4 5

    // 如果想要在循环的过程中修改值，得用引用
    for (auto &i : values) {
        cout << i << " ";
    }
    cout << endl;  // 1 2 3 4 5

    // 迭代器，实际上用的是指针
    for (auto i = values.begin(); i != values.end(); i++) {
        cout << *i << " ";
    }  // 1 2 3 4 5

    return 0;
}
```

## 五、添加元素

在 vector 容器尾部添加一个元素，涉及两个成员函数 push_back() emplace_back()，emplace_back是c++11新加的。

```c++
vector<int> values{};  // 1 2
values.push_back(1);
values.push_back(2);

vector<int> nums{};  // 1 2
nums.emplace_back(1);
nums.emplace_back(2);
```

**emplace_back() 和 push_back() 的底层实现机制不同**

- push_back() 向容器尾部添加元素时，首先会创建这个元素，然后再将这个元素拷贝或者移动到容器中（如果是拷贝的话，事后会自行销毁先前创建的这个元素）；
- emplace_back() 在实现时，则是直接在容器尾部创建这个元素，省去了拷贝或移动元素的过程。

**emplace_back() 的执行效率比 push_back() 高**。因此，在实际使用时，建议大家优先选用 emplace_back()

## 六、插入元素

**insert() 函数是在 vector 容器的指定位置插入一个或多个元素，**常用的有下面四种用法

```c++
vector<int> nums{1, 2};
//迭代器正向 idx=1 的位置上插入
nums.insert(nums.begin() + 1, 3);  // 1 3 2

//迭代器逆向 idx=-2 的位置上插入
nums.insert(nums.end(), 2, 5);  // 1 3 2 5 5

//在末尾添加另一个容器
array<int, 3> n2{7, 8, 9};
nums.insert(nums.end(), n2.begin(), n2.end());  // 1 3 2 5 5 7 8 9

//在末尾添加一组数据
nums.insert(nums.end(), {10, 11});  // 1 3 2 5 5 7 8 9 10 11
```

**emplace() 在 vector 容器指定位置插入一个新的元素。**是 C++11 标准新增加的成员函数

```c++
vector<int> nums{1, 2};
nums.emplace(nums.begin() + 1, 3);  // 1 3 2
```

- insert() 函数向 vector 容器中插入 testDemo 类对象，需要调用类的构造函数和移动构造函数
- emplace() 在插入元素时，是在容器的指定位置直接构造元素

因此，在实际使用中，推荐大家优先使用 emplace()

## 七、删除元素

删除 vector 容器的元素可以借助本身提供的成员函数，还可以借助一些全局函数

| 函数                  | 功能                                                         |
| --------------------- | ------------------------------------------------------------ |
| pop_back()            | 删除 vector 容器中最后一个元素，该容器的大小（size）会减 1，但容量（capacity）不会发生改变。 |
| erase(pos)            | 删除 vector 容器中 pos 迭代器指定位置处的元素，并返回指向被删除元素下一个位置元素的迭代器。该容器的大小（size）会减 1，但容量（capacity）不会发生改变。 |
| swap(beg)、pop_back() | 先调用 swap() 函数交换要删除的目标元素和容器最后一个元素的位置，然后使用 pop_back() 删除该目标元素。 |
| erase(beg,end)        | 删除 vector 容器中位于迭代器 [beg,end)指定区域内的所有元素，并返回指向被删除区域下一个位置元素的迭代器。该容器的大小（size）会减小，但容量（capacity）不会发生改变。 |
| clear()               | 删除 vector 容器中所有的元素，使其变成空的 vector 容器。该函数会改变 vector 的大小（变为 0），但不是改变其容量。 |
| remove() 公共函数     | 删除容器中所有和指定元素值相等的元素，并返回指向最后一个元素下一个位置的迭代器。值得一提的是，调用该函数不会改变容器的大小和容量。需要导入 <algorithm> |

```c++
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> nums{1, 2, 3, 4, 5};
    // 删除最后一个元素
    nums.pop_back();                                  // 1 2 3 4
    cout << "size: " << nums.size() << endl;          // 4
    cout << "capacity: " << nums.capacity() << endl;  // 5

    // 迭代器删除指定位置，指定区间
    nums.erase(nums.begin() + 1);          // 1 3 4
    nums.erase(nums.begin(), nums.end());  //

    // 清空容器
    nums = {1, 1, 5};
    nums.clear();  //

    // 公共函数 remove 删除，指定区间内与指定值相同的元素
    vector<int> demo = {1, 1, 2, 3};
    auto iter = remove(demo.begin(), demo.end(), 1);     // 2 3 2 3
    demo.erase(iter, demo.end());                        // 2 3
    cout << "size is :" << demo.size() << endl;          // 2
    cout << "capacity is :" << demo.capacity() << endl;  // 4
    return 0;
}
```

## 八、capacity 和 size 属性区别

在 STL 中，拥有 capacity 属性的容器只有 vector 和 string

**size** 是当前 vector 容器真实占用的大小，也就是容器当前拥有多少个容器。

**capacity** 是指在发生 realloc 前能允许的最大元素数，即预分配的内存空间。

使用 **resize()** ，size 和 capacity 都变化到指定大小；容器内的对象内存空间是真正存在的。

使用 **reserve()** ，只修改 capacity 的值；容器内的对象并没有真实的内存空间(空间是"野"的)。

```c++
#include <iostream>
#include <vector>

using namespace std;

int main(void)
{
   vector<int> vec;
   cout << "size: " << vec.size() << " capacity: " << vec.capacity() << endl;
   // size: 0 capacity: 0

   vec.push_back(0);
   cout << "size: " << vec.size() << " capacity: " << vec.capacity() << endl;
   // size: 1 capacity: 1

   vec.reserve(10);
   cout << "size: " << vec.size() << " capacity: " << vec.capacity() << endl;
   // size: 1 capacity: 10

   vec.resize(10);
   cout << "size: " << vec.size() << " capacity: " << vec.capacity() << endl;
   // size: 10 capacity: 10

   vec.push_back(0);
   cout << "size: " << vec.size() << " capacity: " << vec.capacity() << endl;
   // size: 11 capacity: 20

   return 0;
}
```
