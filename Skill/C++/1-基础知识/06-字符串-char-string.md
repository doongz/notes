# 字符串-char-string

## 一、C 风格字符串

char 本质上还是 int，char 单个字符单引号，string 双引号

```c++
#include <iostream>
using namespace std;

int main() {
    char c_zero = '0';
    int zero = c_zero;

    int one = '1';
    int nine = '9';

    int a = 'a';
    int z = 'z';
    int A = 'A';
    int Z = 'Z';

    cout << zero << endl;  // 48
    cout << one << endl;   // 49
    cout << a << endl;     // 97
    cout << z << endl;     // 122
    cout << A << endl;     // 65
    cout << Z << endl;     // 90
    return 0;
}
```

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

| 函数            | 描述                                                         |
| --------------- | ------------------------------------------------------------ |
| strcpy(s1, s2); | 复制字符串 s2 到字符串 s1                                    |
| strcat(s1, s2); | 连接字符串 s2 到字符串 s1 的末尾。连接字符串也可以用 **+** 号 |
| strlen(s1);     | 返回字符串 s1 的长度                                         |
| strcmp(s1, s2); | 如果 s1 和 s2 是相同的，则返回 0；如果 s1<s2 则返回值小于 0；如果 s1>s2 则返回值大于 0。 |
| strchr(s1, ch); | 返回一个指针，指向字符串 s1 中字符 ch 的第一次出现的位置     |
| strstr(s1, s2); | 返回一个指针，指向字符串 s1 中字符串 s2 的第一次出现的位置   |

## 二、C++ 中的 String 类（常用）

C++ 标准库提供了 **string** 类类型，支持上述所有的操作，另外还增加了其他更多的功能。

C++ 的 string 可以修改字符串中的内容，python 和 golang 不可以

需引入头文件 `<string>`

| 方法                 | 描述                                              |
| -------------------- | ------------------------------------------------- |
| s.length()           | 返回字符串长度                                    |
| s.insert(2, "bb")    | 在指定下标插入字符串                              |
| s.erase(5)           | 删除指定下标后的元素，可指定删除数量              |
| s.substr(5)          | 提取指定下标后的元素，可指定提取数量              |
| s.find("aa")         | 待查找指定子串，可指定开始查找的下标              |
| s.rfind("aa", 5)     | 最多查找到第二个参数处                            |
| s1.find_first_of(s1) | 查找 s1 和 s2 中第一次相同的字符 ，在 s1 中的下标 |
| **s.push_back()**    | **往字符串后面拼接**                              |

### 1、初始化和赋值

```c++
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s1;
    string s2 = "hello world";
    string s3 = s2;
    string s4(3, 'd');                         // 只能一个字符，只能单引号
    cout << s1 << " " << s1.length() << endl;  // "" 0
    cout << s2 << " " << s2.length() << endl;  // "hello world" 11
}
```

### 2、访问

```c++
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s1 = "hello";
    for (int i = 0; i < s1.length(); i++) {
        cout << s1[i] << ",";
    }
    cout << endl;  // h,e,l,l,o,
}
```

### 3、修改

```c++
string s = "hello";
s[0] = 'H';
cout << s << endl; // Hello
```

### 4、拼接

```c++
string s1 = "hello";
string s2 = s1 + " world";
cout << s2 << endl;  // hello world
```

### 5、插入字符串

第一个参数 为插入下标；第二个参数 为插入的字符串

```c++
string s1 = "aaaa";
s1.insert(2, "bb");
cout << s1 << endl;  // aabbaa
```

### 6、删除字符串

s3.erase(5, 2) 表示，从第 5 个位置开始删，删除两个元素停下来，拼接上后面剩余的

或者理解为，前面保留 5 个，然后删 2 个，再接上后面剩的

```c++
string s1, s2, s3;
s1 = s2 = s3 = "1234567890";
s2.erase(5);
s3.erase(5, 2);
cout << s1 << endl;  // 1234567890
cout << s2 << endl;  // 12345
cout << s3 << endl;  // 12345890
```

### 7、提取子串

s1.substr(5, 2) 表示，从第五个位置开始提取，提取两个元素（前面剔除 5 个，再选取 2 个）

```c++
string s1 = "1234567890";
string s2 = s1.substr(5);
string s3 = s1.substr(5, 2);
cout << s1 << endl;  // 1234567890
cout << s2 << endl;  // 67890
cout << s3 << endl;  // 67
```

### 8、查找

`s1.find(s2, 5)`  第一个参数为待查找的子字符串，第二个参数为开始查找的下标；如不指明，则从第0个字符开始查找。

如果没有查找到子字符串，那么会返回个很大的数

```c++
string s1 = "first second third";
cout << s1.find("second", 5) << endl;  // 6
cout << s1.find("aaa", 5) << endl;     // 18446744073709551615
```

` rfind()` 函数则最多查找到第二个参数处，

如果到了第二个参数所指定的下标还没有找到子字符串，则返回一个无穷大值

```c++
string s1 = "first second third";
cout << s1.rfind("second", 5) << endl;  // 18446744073709551615
```

`find_first_of()` 函数用于查找 s1 和 s2 中第一次相同的 **字符** ，在 s1 中的下标

```c++
string s1 = "first second second third";
string s2 = "asd";
cout << s1.find_first_of(s2) << endl;  // 3
```

### 9、字典序

c\c++中字符串字典序比较函数的区别

```c
// c
char* s1;
char* s2;

if (strcmp(s1, s2) < 0) {
	// s1 的字典序大
}
```

```c++
// c++
string s1;
string s2;

if (s1.compare(s2) > 0) {
	// s2 的字典序大
}
```

## 三、格式转换

### 1、查看格式

```c++
#include <iostream>
#include <typeinfo>
#include <vector>
using namespace std;

int main() {
    int a = 1;
    char c = '1';
    string str = "123";
    vector<int> vec = {1, 2, 3};

    cout << typeid(a).name() << endl;       // i
    cout << typeid(c).name() << endl;       // c
    cout << typeid(str).name() << endl;     // NSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEE
    cout << typeid(str[0]).name() << endl;  // c 字符串string 是由 char 组成的
    cout << typeid(vec).name() << endl;     // NSt3__16vectorIiNS_9allocatorIiEEEE

    cout << c + 1 << endl;  // 50 char 其实也是整形

    return 0;
}
```

### 2、string -> int

```c++
int atoi(const char* str)  // 要先使用 str.c_str() 转化后才能使用
int stoi(const string* str)
```

```c++
#include <iostream>
#include <string>

using namespace std;

int main() {
    string str1 = "123";
    string str2 = "456";
    cout << atoi(str1.c_str()) << endl;  // 123
    cout << stoi(str2) << endl;          // 456
}
```

### 3、string -> char

字符串string 是由 char 组成的，所以直接去值就好

```c++
string str = "123";
char c = str[0];
```

### 4、char -> int

char 就是 int

```c++
char a = 'a';
int a_int = a;
cout << a_int << endl;  // 97
```

### 5、char / int -> string

string to_string (int val);

```c++
int a = 123;
string b = to_string(a);
cout << b << endl;  // "123"
```

### 6、类似 python ord() 实现

```c++
string s = "";
s += 'a' + 2;
cout << s << endl; // c
```

