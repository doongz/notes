# 向量 vector

向量容器（一个 C++ 标准的模板），它与数组十分相似

不同的是，向量在需要扩展大小的时候，会自动处理它自己的存储需求

```c++
#include <iostream>
#include <vector>
using namespace std;

int main()
{
   vector<int> vec;            // 创建一个向量存储 int
   cout << vec.size() << endl; // vec 的原始大小为 0

   // 推入 5 个值到向量中
   for (int i = 0; i < 5; i++)
   {
      vec.push_back(i);
   }
   cout << vec.size() << endl; // vec 扩展后的大小为 5

   // 访问向量中的 5 个值
   for (int i = 0; i < 5; i++)
   {
      cout << vec[i] << " "; // 0 1 2 3 4
   }
   cout << endl;

   // 使用迭代器 iterator 访问值
   vector<int>::iterator v = vec.begin();
   while (v != vec.end())
   {
      cout << *v << " "; // 0 1 2 3 4
      v++;
   }

   return 0;
}
```

### capacity 和 size 属性区别

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

## 打印 vector

https://zhuanlan.zhihu.com/p/67447529
