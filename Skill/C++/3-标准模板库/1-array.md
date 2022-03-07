# array

array 容器在 C++ 普通数组的基础上，添加了一些成员函数和全局函数。在使用上，它比普通数组更安全，且效率并没有因此变差。

**array 容器的大小是固定的，无法动态的扩展或收缩**

```c++
#include <array>
#include <iostream>
using namespace std;

int main() {
    //初始化 values 容器为 {0,1,2,3}
    array<int, 4> values{};
    for (int i = 0; i < values.size(); i++) {
        values.at(i) = i;
    }

    //使用 get() 重载函数输出指定位置元素
    cout << get<3>(values) << endl;
    
    //如果容器不为空，则输出容器中所有的元素
    if (!values.empty()) {
        for (auto val = values.begin(); val < values.end(); val++) {
            cout << *val << " ";
        }
    }
}
```

如下创建 array 容器的方式，可以将所有的元素初始化为 0 或者和默认元素类型等效的值：

```c++
std::array<double, 10> values {};
```

## 一、成员函数

| 成员函数            | 功能                                                         |
| ------------------- | ------------------------------------------------------------ |
| **begin()**         | **返回指向容器中第一个元素的随机访问迭代器**                 |
| **end()**           | **返回指向容器最后一个元素之后一个位置的随机访问迭代器，通常和 begin() 结合使用** |
| rbegin()            | 返回指向最后一个元素的随机访问迭代器。                       |
| rend()              | 返回指向第一个元素之前一个位置的随机访问迭代器。             |
| cbegin()            | 和 begin() 功能相同，只不过在其基础上增加了 const 属性，不能用于修改元素。 |
| cend()              | 和 end() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。 |
| crbegin()           | 和 rbegin() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。 |
| crend()             | 和 rend() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改元素。 |
| **size()**          | **返回容器中当前元素的数量，其值始终等于初始化 array 类的第二个模板参数 N** |
| max_size()          | 返回容器可容纳元素的最大数量，其值始终等于初始化 array 类的第二个模板参数 N。 |
| empty()             | 判断容器是否为空，和通过 size()==0 的判断条件功能相同，但其效率可能更快。 |
| **at(n)**           | **返回容器中 n 位置处元素的引用，该函数自动检查 n 是否在有效的范围内，如果不是则抛出 out_of_range 异常** |
| front()             | 返回容器中第一个元素的直接引用，该函数不适用于空的 array 容器。 |
| back()              | 返回容器中最后一个元素的直接应用，该函数同样不适用于空的 array 容器。 |
| data()              | 返回一个指向容器首个元素的[指针](http://c.biancheng.net/c/80/)。利用该指针，可实现复制容器中所有元素等类似功能。 |
| fill(val)           | 将 val 这个值赋值给容器中的每个元素。                        |
| array1.swap(array2) | 交换 array1 和 array2 容器中的所有元素，但前提是它们具有相同的长度和类型。 |

## 二、随机访问迭代器

**begin() 和 end() 成员函数返回的是正向迭代器**，它们分别指向「首元素」和「尾元素+1」 的位置。

在实际使用时，我们可以利用它们实现初始化容器或者遍历容器中元素的操作。

```c++
#include <array>
#include <iostream>
using namespace std;

int main() {
    array<int, 5> values;
    auto first = values.begin();
    auto last = values.end();
    int h = 1;

    //初始化 values 容器为{1,2,3,4,5}
    while (first != last) {
        *first = h;
        first++;
        h++;
    }
    // 循环打印 1 2 3 4 5
    first = values.begin();
    while (first != last) {
        cout << *first << " ";
        first++;
    }
    return 0;
}
```

**rbegin()/rend() 成员函数返回的是反向迭代器**，它们每对都可以分别得到指向最一个元素和第一个元素前一个位置的随机访问迭代器

需要注意的是，在使用反向迭代器进行 ++ 或 -- 运算时，**++ 指的是迭代器向左移动一位，-- 指的是迭代器向右移动一位**，即这两个运算符的功能也“互换”了

```c++
#include <array>
#include <iostream>
using namespace std;

int main() {
    array<int, 5> values;

    //初始化 values 容器为 {5,4,3,2,1}
    int v = 1;
    for (auto first = values.begin(); first != values.end(); first++) {
        *first = v;
        v++;
    }
    // 逆序输出 5 4 3 2 1
    for (auto first = values.rbegin(); first != values.rend(); first++) {
        cout << *first << " ";
    }
    return 0;
}
```

## 三、访问元素

### 1、单个元素

可以通过`容器名[]`的方式直接访问和使用容器中的元素，**但是此方法没有做任何边界检查，使用越界的索引值去访问或存储元素，也不会被检测到报错**

没有实现边界检查的功能呢？性能，如果每次访问元素，都去检查索引值，无疑会产生很多开销。**所以确定不会越界的时候使用这个方法，就能避免这种开销**。

```c++
values[4] = values[3] + 2.O*values[1];
```

为了能够有效地避免越界访问的情况，可以使用 array 容器提供的 at() 成员函数

```c++
values.at(4) = values.at(3) + 2.O*values.at(1);
```

array 容器还提供了 get<n> 模板函数，它是一个辅助函数，能够获取到容器的第 n 个元素

需要注意的是，该模板函数中，**参数的实参必须是一个在编译时可以确定的常量表达式，不能是一个循环变量**。也就是说，它只能访问模板参数指定的元素，编译器在编译时会对它进行检查。

```c++
array<int, 5> values{1, 2, 3, 4, 5};
cout << get<3>(values) << endl;  // 4
// cout << get<9>(values) << endl;  // 越界，会发生编译错误
```

### 2、多个元素

for (int i = 0; i < values.size(); i++)

for (auto &i : values) 

for (auto i = values.begin(); i != values.end(); i++) 

```c++
#include <array>
#include <iostream>
using namespace std;

int main() {
    array<int, 5> values{1, 2, 3, 4, 5};

    for (int i = 0; i < values.size(); i++) {
        cout << values[i] << " ";
    }  // 1 2 3 4 5
    cout << endl;

    // 如果仅输出元素值，加不加引用效果一样
    // 如果想在遍历的过程中改变元素的值，加上引用 &
    for (auto &i : values) {
        cout << i << " ";
    }  // 1 2 3 4 5
    cout << endl;

    // 使用迭代器，变量 i 是指针
    for (auto i = values.begin(); i != values.end(); i++) {
        cout << *i << " ";
    }  // 1 2 3 4 5
    return 0;
}
```

