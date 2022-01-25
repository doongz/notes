# map 容器

map 容器存储的都是 pair 类型的键值对元素，更确切的说**，map 容器存储的都是 pair<const K, T> 类型的键值对元素**。各个键值对的键和值可以是基本数据类型（int、double 等）、使用结构体或类自定义的类型。

> 通常情况下，map 容器中存储的各个键值对都选用 string 字符串作为键的类型。

与此同时，**在使用 map 容器存储多个键值对时，该容器会自动根据各键值对的键的大小，按照既定的规则进行排序。**默认情况下，map 容器选用`std::less<T>`排序规则（其中 T 表示键的数据类型），其会根据键的大小对所有键值对做升序排序。当然，根据实际情况的需要，我们可以手动指定 map 容器的排序规则，既可以选用 STL 标准库中提供的其它排序规则（比如`std::greater<T>`），也可以自定义排序规则。

另外需要注意的是，使用 map 容器存储的各个键值对，**键的值既不能重复也不能被修改**。换句话说，map 容器中存储的各个键值对不仅键的值独一无二，键的类型也会用 const 修饰，这意味着只要键值对被存储到 map 容器中，其键的值将不能再做任何修改。

map 容器定义在 <map> 头文件中，并位于 std 命名空间中。

## 一、创建

```c++
#include <iostream>
#include <map>
using namespace std;

int main() {
    map<string, int> m1;
    map<string, int> m2{{"a", 1}, {"b", 2}, {"c", 3}};

    // 拷贝（复制）构造函数
    map<string, int> m3(m2);
    
    // 指定区域内的键值对
    map<string, int> m4(m2.begin()++, m2.end());

    // 指定排序规则
    map<string, int, less<string>> m5{{"a", 1}, {"b", 2}, {"c", 3}};
}
```

## 二、成员方法

| 成员方法             | 功能                                                         |
| -------------------- | ------------------------------------------------------------ |
| **begin()**          | **返回指向容器中第一个（注意，是已排好序的第一个）键值对的双向迭代器。如果 map 容器用 const 限定，则该方法返回的是 const 类型的双向迭代器。** |
| **end()**            | **返回指向容器最后一个元素（注意，是已排好序的最后一个）所在位置后一个位置的双向迭代器，通常和 begin() 结合使用。如果 map 容器用 const 限定，则该方法返回的是 const 类型的双向迭代器。** |
| rbegin()             | 返回指向最后一个（注意，是已排好序的最后一个）元素的反向双向迭代器。如果 map 容器用 const 限定，则该方法返回的是 const 类型的反向双向迭代器。 |
| rend()               | 返回指向第一个（注意，是已排好序的第一个）元素所在位置前一个位置的反向双向迭代器。如果 map 容器用 const 限定，则该方法返回的是 const 类型的反向双向迭代器。 |
| cbegin()             | 和 begin() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改容器内存储的键值对。 |
| cend()               | 和 end() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改容器内存储的键值对。 |
| crbegin()            | 和 rbegin() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改容器内存储的键值对。 |
| crend()              | 和 rend() 功能相同，只不过在其基础上，增加了 const 属性，不能用于修改容器内存储的键值对。 |
| find(key)            | 在 map 容器中查找键为 key 的键值对，如果成功找到，则返回指向该键值对的双向迭代器；反之，则返回和 end() 方法一样的迭代器。另外，如果 map 容器用 const 限定，则该方法返回的是 const 类型的双向迭代器。 |
| **lower_bound(key)** | **返回一个指向当前 map 容器中第一个大于或等于 key 的键值对的双向迭代器。如果 map 容器用 const 限定，则该方法返回的是 const 类型的双向迭代器。** |
| **upper_bound(key)** | **返回一个指向当前 map 容器中第一个大于 key 的键值对的迭代器。如果 map 容器用 const 限定，则该方法返回的是 const 类型的双向迭代器。** |
| equal_range(key)     | 该方法返回一个 pair 对象（包含 2 个双向迭代器），其中 pair.first 和 lower_bound() 方法的返回值等价，pair.second 和 upper_bound() 方法的返回值等价。也就是说，该方法将返回一个范围，该范围中包含的键为 key 的键值对（map 容器键值对唯一，因此该范围最多包含一个键值对）。 |
| **empty()**          | **若容器为空，则返回 true；否则 false。**                    |
| **size()**           | **返回当前 map 容器中存有键值对的个数。**                    |
| max_size()           | 返回 map 容器所能容纳键值对的最大个数，不同的操作系统，其返回值亦不相同。 |
| operator[]           | map容器重载了 [] 运算符，只要知道 map 容器中某个键值对的键的值，就可以向获取数组中元素那样，通过键直接获取对应的值。 |
| at(key)              | 找到 map 容器中 key 键对应的值，如果找不到，该函数会引发 out_of_range 异常。 |
| insert()             | 向 map 容器中插入键值对。                                    |
| erase()              | 删除 map 容器指定位置、指定键（key）值或者指定区域内的键值对。后续章节还会对该方法做重点讲解。 |
| swap()               | 交换 2 个 map 容器中存储的键值对，这意味着，操作的 2 个键值对的类型必须相同。 |
| clear()              | 清空 map 容器中所有的键值对，即使 map 容器的 size() 为 0。   |
| emplace()            | 在当前 map 容器中的指定位置处构造新键值对。其效果和插入键值对一样，但效率更高。 |
| emplace_hint()       | 在本质上和 emplace() 在 map 容器中构造新键值对的方式是一样的，不同之处在于，使用者必须为该方法提供一个指示键值对生成位置的迭代器，并作为该方法的第一个参数。 |
| **count(key)**       | **在当前 map 容器中，查找键为 key 的键值对的个数并返回**     |

## 三、双向迭代器

标准库为 map 容器配备的是双向迭代器（bidirectional iterator）。这意味着，map 容器迭代器只能进行 ++p、p++、--p、p--、*p 操作，并且迭代器之间只能使用 == 或者 != 运算符进行比较。

```c++
map<string, int> m{{"a", 1}, {"b", 2}, {"c", 3}};
for (auto it = m.begin(); it != m.end(); it++) {
    cout << it->first << " : " << it->second << endl;
}
// a : 1
// b : 2
// c : 3
for (auto it = m.rbegin(); it != m.rend(); it++) {
    cout << it->first << " : " << it->second << endl;
}
// c : 3
// b : 2
// a : 1
```

find() 成员方法，它能帮我们查找指定 key 值的键值对，如果成功找到，则返回一个指向该键值对的双向迭代器

```c++
map<string, int> m{{"a", 1}, {"b", 2}, {"c", 3}};
auto first = m.find("b");
for (; first != m.end(); first++) {
    cout << first->first << " : " << first->second << endl;
}
// b : 2
// c : 3
```

## 四、获取键对应值

几乎在所有使用 map 容器的场景中，都是从该容器中找到某个键对应的值

1) map 类模板中对`[ ]`运算符进行了重载，通过指定的键，获取 map 容器中该键对应的值。也可向该 map 容器中增添一个键值对，但要保证新添加键值对的键和当前 map 容器中已存储的键值对的键都不一样

```c++
map<string, int> m{{"a", 1}, {"b", 2}};
cout << m["a"] << endl;  // 1

m["c"] = 3;
m["b"] = 2;
for (auto it = m.begin(); it != m.end(); it++) {
    cout << it->first << " : " << it->second << endl;
}
// a : 1
// b : 2
// c : 3
```

2) 使用 at() 成员方法。如果在当前容器中查找失败，会抛出 out_of_range 异常。

```c++
map<string, int> m{{"a", 1}, {"b", 2}};
cout << m.at("a") << endl;  // 1
// cout << m.at("c") << endl;  // 报错
```

3) 遍历整个 map 容器

```c++
map<string, int> m{{"a", 1}, {"b", 2}, {"c", 3}};
for (auto it = m.begin(); it != m.end(); it++) {
    cout << it->first << " : " << it->second << endl;
}
// a : 1
// b : 2
// c : 3
```

## 五、插入数据

```c++
map<string, int> m{{"a", 1}};

//获取已存储键值对中，指定键对应的值
cout << m["a"] << endl;  // 1
//向 map 容器添加新键值对
m["b"] = 2;
//修改 map 容器已存储键值对中，指定键对应的值
m["a"] = 3;

for (auto it = m.begin(); it != m.end(); it++) {
    cout << it->first << " : " << it->second << endl;
}
// a : 3
// b : 2
```

map 类模板中还提供有 [insert() 成员方法](http://c.biancheng.net/view/7196.html)

insert() 方法可以将新的键值对插入到 map 容器中的指定位置，但这与 map 容器会自动对存储的键值对进行排序并不冲突。当使用 insert() 方法向 map 容器的指定位置插入新键值对时，其底层会先将新键值对插入到容器的指定位置，如果其破坏了 map 容器的有序性，该容器会对新键值对的位置进行调整。

map 类模板中还提供了 [emplace() 和 emplace_hint() 成员函数](http://c.biancheng.net/view/7182.html)，也可以实现向 map 容器中插入新的键值对

实现相同的插入操作，无论是用 emplace() 还是 emplace_hont()，都比 insert() 方法的效率高

## 六、multimap 容器

multimap 容器具有和 map 相同的特性，也用于存储 pair<const K, T> 类型的键值对，其中各个键值对的键的值不能做修改；也会自行根据键的大小对存储的所有键值对做排序操作。

**和 map 容器的区别在于，multimap 容器中可以同时存储多（≥2）个键相同的键值对。**

```c++
#include <iostream>
#include <map>  //map
using namespace std;

int main() {
    multimap<string, int> m{
        {"a", 1},
        {"b", 2},
        {"c", 3},
        {"a", 2},
        {"b", 2}};

    for (auto it = m.begin(); it != m.end(); it++) {
        cout << it->first << " : " << it->second << endl;
    }
    // a : 1
    // a : 2
    // b : 2
    // b : 2
    // c : 3

    // 拷贝（复制）构造函数
    multimap<string, int> m1(m);

    // 选定某块区域内的所有键值对
    multimap<string, int> m2(m.begin()++, m.end());

    // 指定排列顺序
    multimap<string, int, greater<string>> m3{
        {"a", 1},
        {"b", 2},
        {"c", 3},
        {"a", 2},
        {"b", 2}};
    // c : 3
    // b : 2
    // b : 2
    // a : 1
    // a : 2

    return 0;
}
```

和 map 容器相比，multimap 未提供 at() 成员方法，也没有重载 [] 运算符。这意味着，map 容器中通过指定键获取指定指定键值对的方式，将不再适用于 multimap 容器。其实这很好理解，因为 multimap 容器中指定的键可能对应多个键值对，而不再是 1 个。

由于 multimap 容器可存储多个具有相同键的键值对，因此表 1 中的 lower_bound()、upper_bound()、equal_range() 以及 count() 成员方法会经常用到。

```c++
multimap<string, int> m{
    {"a", 1},
    {"b", 2},
    {"b", 2},
    {"b", 3},
    {"c", 1}};
auto first = m.lower_bound("b");
auto end = m.upper_bound("b");

cout << first->first << " : " << first->second << endl;  // b : 2
cout << end->first << " : " << end->second << endl;      // c : 1

while (first != end) {
    cout << first->first << " : " << first->second << endl;
    first++;
}
// b : 2
// b : 2
// b : 3
```

