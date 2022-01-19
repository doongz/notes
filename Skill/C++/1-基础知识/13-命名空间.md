# 命名空间

一个中大型软件往往由多名程序员共同开发，会使用大量的变量和函数，不可避免地会出现变量或函数的命名冲突。当所有人的代码都测试通过，没有问题时，将它们结合到一起就有可能会出现命名冲突。

为了解决合作开发时的命名冲突问题，引入了**命名空间（Namespace）**的概念。

```c++
namespace name{
    //variables, functions, classes
}
```

`name`是命名空间的名字，它里面可以包含变量、函数、类、typedef、#define 等，也可以再包含命名空间，最后由`{ }`包围

## using 和 :: 

使用 `using namespace first_space;` ，这个指令会告诉编译器，后续的代码将使用指定的命名空间中的名称

通过 `second_space::func();` ，指定命名空间内的元素

```c++
#include <iostream>
using namespace std;

namespace first_space {
void func() {
    cout << "Inside first_space" << endl;
}
}  // namespace first_space

namespace second_space {
void func() {
    cout << "Inside second_space" << endl;
}
}  // namespace second_space

using namespace first_space;

int main() {
    func();                // Inside first_space
    second_space::func();  // Inside second_space
    return 0;
}
```

using 指令也可以用来指定命名空间中的特定项目。例如，只打算使用 std 命名空间中的 cout 部分

```c++
#include <iostream>
using std::cout;

int main() {
    cout << "ok" << std::endl;
    return 0;
}
```

## 不连续的命名空间

一个命名空间的各个组成部分可以分散在多个文件中，使用相同的命名就行

所以，命名空间定义可以是定义一个新的命名空间，也可以是为已有的命名空间增加新的元素

## 嵌套的命名空间

```c++
#include <iostream>
using namespace std;

namespace first_space {
    void func() {
        cout << "First" << endl;
    }
    namespace second_space {
        void func() {
            cout << "Second" << endl;
        }
    }  // namespace second_space
}  // namespace first_space

using namespace first_space::second_space;

int main() {
    func();               // Second
    first_space::func();  // First
    func();               // Second
    return 0;
}
```

