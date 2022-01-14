# 字符串-char-string

## C 风格字符串

C 风格的字符串起源于 C 语言，并在 C++ 中继续得到支持。

字符串实际上是使用 **null** 字符 **\0** 终止的一维字符数组。由于在数组的末尾存储了空字符，所以字符数组的大小比原字符数多一个。

```c++
#include <iostream>
using namespace std;

int main()
{
   char site[7] = {'R', 'U', 'N', 'O', 'O', 'B', '\0'};
   // 编译器会在初始化数组时，自动把 \0 放在字符串的末尾
   char name[] = "dodo";

   cout << site << endl; // "RUNOOB"
   cout << name << endl; // "dodo"

   return 0;
}
```

| 函数                | 描述                                                         |
| ------------------- | ------------------------------------------------------------ |
| **strcpy(s1, s2);** | 复制字符串 s2 到字符串 s1                                    |
| **strcat(s1, s2);** | 连接字符串 s2 到字符串 s1 的末尾。连接字符串也可以用 **+** 号 |
| **strlen(s1);**     | 返回字符串 s1 的长度                                         |
| **strcmp(s1, s2);** | 如果 s1 和 s2 是相同的，则返回 0；如果 s1<s2 则返回值小于 0；如果 s1>s2 则返回值大于 0。 |
| **strchr(s1, ch);** | 返回一个指针，指向字符串 s1 中字符 ch 的第一次出现的位置     |
| **strstr(s1, s2);** | 返回一个指针，指向字符串 s1 中字符串 s2 的第一次出现的位置   |



## C++ 中的 String 类（常用）

C++ 标准库提供了 **string** 类类型，支持上述所有的操作，另外还增加了其他更多的功能。

需引入头文件 `<string>`

```c++
#include <iostream>
#include <string>

using namespace std;

int main()
{
   string str1 = "runoob";
   string str2 = "google";
   string str3;
   int len;

   // 复制 str1 到 str3
   str3 = str1;
   cout << "str3 : " << str3 << endl; // runoob

   // 连接 str1 和 str2
   str3 = str1 + str2;
   cout << "str1 + str2 : " << str3 << endl; // runoobgoogle

   // 连接后，str3 的总长度
   len = str3.size();
   cout << "str3.size() :  " << len << endl; // 12

   return 0;
}
```

