# unordered_map

unordered_map 容器和 map 容器一样，以键值对（pair类型）的形式存储数据，存储的各个键值对的键互不相同且不允许被修改。但由于 unordered_map 容器底层采用的是哈希表存储结构，该结构本身不具有对数据的排序功能，所以此容器内部不会自行对存储的键值对进行排序。

unordered_map 容器在`<unordered_map>`头文件中，并位于 std 命名空间中

## 一、创建

``` c++
#include <iostream>
#include <string>
#include <unordered_map>
using namespace std;

int main() {
    // 1 调用 unordered_map 模板类的默认构造函数
    unordered_map<string, int> um1;

    // 2 在创建的同时，完成初始化操作
    unordered_map<string, int> um2{{"a", 1}, {"b", 2}, {"c", 3}};
    // b : 2
    // c : 3
    // a : 1

    // 3 复制（拷贝）构造函数
    unordered_map<string, int> um3(um2);

    // 4 部分复制
    unordered_map<string, int> um4(++um2.begin(), um2.end());
    // a : 1
    // c : 3

    return 0;
}
```

## 二、成员方法

| 成员方法               | 功能                                                         |
| ---------------------- | ------------------------------------------------------------ |
| **begin()**            | **返回指向容器中第一个键值对的正向迭代器**                   |
| **end()**              | **返回指向容器中最后一个键值对之后位置的正向迭代器**         |
| cbegin()               | 和 begin() 功能相同，只不过在其基础上增加了 const 属性，即该方法返回的迭代器不能用于修改容器内存储的键值对。 |
| cend()                 | 和 end() 功能相同，只不过在其基础上，增加了 const 属性，即该方法返回的迭代器不能用于修改容器内存储的键值对。 |
| empty()                | 若容器为空，则返回 true；否则 false。                        |
| size()                 | 返回当前容器中存有键值对的个数。                             |
| max_size()             | 返回容器所能容纳键值对的最大个数，不同的操作系统，其返回值亦不相同。 |
| operator[key]          | 该模板类中重载了 [] 运算符，其功能是可以向访问数组中元素那样，只要给定某个键值对的键 key，就可以获取该键对应的值。注意，如果当前容器中没有以 key 为键的键值对，则其会使用该键向当前容器中插入一个新键值对。 |
| at(key)                | 返回容器中存储的键 key 对应的值，如果 key 不存在，则会抛出 out_of_range 异常。 |
| find(key)              | 查找以 key 为键的键值对，如果找到，则返回一个指向该键值对的正向迭代器；反之，则返回一个指向容器中最后一个键值对之后位置的迭代器（如果 end() 方法返回的迭代器）。 |
| **count(key)**         | **在容器中查找以 key 键的键值对的个数。用来检测 key 在不在里面** |
| equal_range(key)       | 返回一个 pair 对象，其包含 2 个迭代器，用于表明当前容器中键为 key 的键值对所在的范围。 |
| emplace()              | 向容器中添加新键值对，效率比 insert() 方法高。               |
| emplace_hint()         | 向容器中添加新键值对，效率比 insert() 方法高。               |
| **insert({key, val})** | **向容器中添加新键值对**                                     |
| **erase(key)**         | **删除指定键值对**                                           |
| clear()                | 清空容器，即删除容器中存储的所有键值对。                     |
| swap()                 | 交换 2 个 unordered_map 容器存储的键值对，前提是必须保证这 2 个容器的类型完全相等。 |
| bucket_count()         | 返回当前容器底层存储键值对时，使用桶（一个线性链表代表一个桶）的数量。 |
| max_bucket_count()     | 返回当前系统中，unordered_map 容器底层最多可以使用多少桶。   |
| bucket_size(n)         | 返回第 n 个桶中存储键值对的数量。                            |
| bucket(key)            | 返回以 key 为键的键值对所在桶的编号。                        |
| load_factor()          | 返回 unordered_map 容器中当前的负载因子。负载因子，指的是的当前容器中存储键值对的数量（size()）和使用桶数（bucket_count()）的比值，即 load_factor() = size() / bucket_count()。 |
| max_load_factor()      | 返回或者设置当前 unordered_map 容器的负载因子。              |
| rehash(n)              | 将当前容器底层使用桶的数量设置为 n。                         |
| reserve()              | 将存储桶的数量（也就是 bucket_count() 方法的返回值）设置为至少容纳count个元（不超过最大负载因子）所需的数量，并重新整理容器。 |
| hash_function()        | 返回当前容器使用的哈希函数对象。                             |

## 三、前向迭代器

unordered_map 容器迭代器的类型为前向迭代器（又称正向迭代器）。这意味着，假设 p 是一个前向迭代器，则其只能进行 *p、p++、++p 操作，且 2 个前向迭代器之间只能用 == 和 != 运算符做比较。

```c++
unordered_map<string, int> um{{"a", 1}, {"b", 2}, {"c", 3}};

// 遍历输出 umap 容器中所有的键值对
for (auto it = um.begin(); it != um.end(); it++) {
    cout << it->first << " : " << it->second << endl;
}

//获取指向指定键值对的前向迭代器
auto it = um.find("a");
cout << it->first << " : " << it->second << endl;  // a : 1
```

简写遍历

```c++
for (int a = 0; a < 5; a++) {
    um[a] = 123123;
}
for (auto &[k, v] : um) {
    cout << k << " : " << v << endl;
}
// 4 : 123123
// 3 : 123123
// 2 : 123123
// 0 : 123123
// 1 : 123123
```

## 四、获取元素

1) unordered_map 容器类模板中，实现了对 [ ] 运算符的重载，使得我们可以像“利用下标访问普通数组中元素”那样，通过目标键值对的键获取到该键对应的值。

如果没有存储指定的元素作为键的键值对，则此时 [ ] 运算符的功能将转变为：向当前容器中添加以目标元素为键的键值对

```c++
#include <iostream>
#include <unordered_map>
using namespace std;

int main() {
    unordered_map<string, int> um{{"a", 1}, {"b", 2}, {"c", 3}};

    int m = um["a"];
    cout << m << endl;  // 1

    // 判断元素在不在map里面
    cout << um.count("b") << endl;  // 1 相当于找到了，返回true
    cout << um.count("d") << endl;  // 0 相当于没有，返回false

    // 使用 um["e"] 有个风险，如果里面没有"e"，就会往里面添加
    cout << um.count("e") << endl;  // 0
    cout << um["e"] << endl;        // 0 值的默认值是0
    cout << um.count("e") << endl;  // 1

    return 0;
}
```

2) unordered_map 类模板中，还提供有 at() 成员方法，和使用 [ ] 运算符一样，at() 成员方法也需要根据指定的键，才能从容器中找到该键对应的值；不同之处在于，如果在当前容器中查找失败，该方法不会向容器中添加新的键值对，而是直接抛出`out_of_range`异常

3) 通过 find() 方法得到的是一个正向迭代器，该迭代器的指向分以下 2 种情况：

1. 当 find() 方法成功找到以指定元素作为键的键值对时，其返回的迭代器就指向该键值对；
2. 当 find() 方法查找失败时，其返回的迭代器和 end() 方法返回的迭代器一样，指向容器中最后一个键值对之后的位置。

4)  begin()/end() 或者 cbegin()/cend()，通过遍历整个容器中的键值对来找到目标键值对

## 五、添加新的键值对

insert() 方法可以将 pair 类型的键值对元素添加到 unordered_map 容器中

该方法的返回值为 pair类型值，内部包含一个 iterator 迭代器和 bool 变量：

- 当 insert() 将 val 成功添加到容器中时，返回的迭代器指向新添加的键值对，bool 值为 True；
- 当 insert() 添加键值对失败时，意味着当前容器中本就存储有和要添加键值对的键相等的键值对，这种情况下，返回的迭代器将指向这个导致插入操作失败的迭代器，bool 值为 False

```c++
unordered_map<string, int> um{{"a", 1}};

auto res = um.insert({"b", 2});
cout << res.first->first << " : " << res.first->second << endl;  // b : 2
cout << res.second << endl;                                      // 1
```

C++ 11 标准也为 unordered_map 容器新增了 emplace() 和 emplace_hint() 成员方法，执行效率会比 insert() 方法高

## 六、删除元素

unordered_map 容器类模板中提供了以下 2 个成员方法：

- erase()：删除 unordered_map 容器中指定的键值对；
- clear()：删除 unordered_map 容器中所有的键值对，即清空容器。

```c++
unordered_map<string, int> um{
    {"a", 1},
    {"b", 2},
    {"c", 3}};

// 删除并返回结果
auto res = um.erase("b");
cout << res << endl;  // 1

auto res2 = um.erase(um.begin());
cout << res2->first << " : " << res2->second << endl;
// c : 3

// 清空键值对
um.clear();
```

## 七、unordered_multimap

unordered_multimap 容器可以存储多个键相等的键值对

无序容器中存储的各个键值对，都会哈希存到各个桶（本质为链表）中。而对于 unordered_multimap 容器来说，其存储的所有键值对中，键相等的键值对会被哈希到同一个桶中存储。

```c++
unordered_multimap<string, int> umm{
    {"a", 1},
    {"b", 2},
    {"b", 2},
    {"c", 3}};

for (auto it = umm.begin(); it != umm.end(); it++) {
    cout << it->first << " : " << it->second << endl;
}
// b : 2
// b : 2
// a : 1
// c : 3
```
