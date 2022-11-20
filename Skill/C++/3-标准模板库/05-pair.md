# pair 类模板

C++ STL 标准库提供了 pair 类模板，其专门用来将 2 个普通元素 first 和 second（可以是 C++ 基本数据类型、结构体、类自定的类型）创建成一个新元素`<first, second>`。通过其构成的元素格式不难看出，使用 pair 类模板来创建“键值对”形式的元素，再合适不过。

## 一、创建

pair 类模板定义在`<utility>`头文件中

```c++
#include <iostream>
#include <string>
#include <utility>  // pair
using namespace std;

int main() {
    pair<string, int> pair1;
    pair1.first = "One";
    pair1.second = 1;
    pair<string, int> pair2("Two", 2);

    cout << pair1.first << " : " << pair1.second << endl;  // One : 1
    cout << pair2.first << " : " << pair2.second << endl;  // Two : 2
    return 0;
}
```

## 二、运算

`<utility>`头文件中除了提供创建 pair 对象的方法之外，还为 pair 对象重载了 <、<=、>、>=、==、!= 这 6 的运算符，其运算规则是：对于进行比较的 2 个 pair 对象，先比较 pair.first 元素的大小，如果相等则继续比较 pair.second 元素的大小。

> 注意，对于进行比较的 2 个 pair 对象，其对应的键和值的类型比较相同，否则将没有可比性，同时编译器提示没有相匹配的运算符，即找不到合适的重载运算符。

```c++
#include <iostream>
#include <string>
#include <utility>  // pair
using namespace std;

int main() {
    pair<string, int> pair1("a", 1);
    pair<string, int> pair2("b", 1);
    pair<string, int> pair3("b", 2);
    cout << (pair1 < pair2) << endl; // 1
    cout << (pair2 < pair3) << endl; // 1
}
```

