# 结构体

**结构体**是 C++ 中另一种用户自定义的可用的数据类型，允许存储不同类型的数据项

```c++
#include <iostream>
#include <cstring>

using namespace std;

// 声明一个结构体类型 Book
struct Book
{
   char title[50];
   int id;
   float stars;
};

int main()
{
   Book bk1; // 定义结构体类型 Book 的变量 bk1
   strcpy(bk1.title, "C-Learning");
   bk1.id = 123;
   bk1.stars = 6.5;

   Book bk2 = {"Python-Learning", 456, 9.6}; // 声明时赋值

   // 输出 bk1 信息
   cout << "title: " << bk1.title << " ";
   cout << "id: " << bk1.id << " ";
   cout << "stars: " << bk1.stars << endl;
   // title: C-Learning id: 123 stars: 6.5

   // 输出 bk2 信息
   cout << "title: " << bk2.title << " ";
   cout << "id: " << bk2.id << " ";
   cout << "stars: " << bk2.stars << endl;
   // title: Python-Learning id: 456 stars: 9.6

   return 0;
}
```

## 结构体作为入参和出参

```c++
#include <iostream>
#include <cstring>

using namespace std;

// 声明一个结构体类型 Book
struct Book
{
   char title[50];
   int id;
   float stars;
};

Book getMaxBook(Book, Book); // 函数声明
// struct Book getMaxBook(struct Book, struct Book); // 也可以加上 struct

Book getMaxBook(Book b1, Book b2)
{
   if (b1.stars > b2.stars)
   {
      return b1;
   }
   return b2;
}

int main()
{
   Book bk1 = {"C-Learning", 123, 6.5};
   Book bk2 = {"Python-Learning", 456, 9.6};

   Book maxbk = getMaxBook(bk1, bk2);
   cout << "title: " << maxbk.title << " ";
   cout << "id: " << maxbk.id << " ";
   cout << "stars: " << maxbk.stars << endl;
   // title: Python-Learning id: 456 stars: 9.6

   return 0;
}
```

## 指向结构体的指针

向结构的指针访问结构的成员，必须使用 -> 运算符

```c++
#include <iostream>
#include <cstring>

using namespace std;

// 声明一个结构体类型 Book
struct Book
{
   char title[50];
   int id;
   float stars;
};

Book *setStars(Book *); // 入参、出参为结构体指针

Book *setStars(Book *book)
{
   book->stars = 10; // 访问结构的成员
   return book;
}

int main()
{
   Book bk1 = {"C-Learning", 123, 6.5};
   Book bk2 = {"Python-Learning", 456, 9.6};

   Book *ptr1 = setStars(&bk1); // Book 类型的指针
   Book *ptr2;
   ptr2 = &bk2;

   cout << "title: " << ptr1->title << " ";
   cout << "id: " << ptr1->id << " ";
   cout << "stars: " << ptr1->stars << endl;
   // title: C-Learning id: 123 stars: 10

   cout << "title: " << ptr2->title << " ";
   cout << "id: " << ptr2->id << " ";
   cout << "stars: " << ptr2->stars << endl;
   // title: Python-Learning id: 456 stars: 9.6

   return 0;
}
```

## typedef 关键字

下面是一种更简单的定义结构的方式，可以为创建的类型取一个"别名"。

```
typedef struct Books
{
   char  title[50];
   char  author[50];
   char  subject[100];
   int   book_id;
}Books;
```

现在，可以直接使用 *Books* 来定义 *Books* 类型的变量，而不需要使用 struct 关键字。**好像现在不用 typedef 也可以不加 struct**

```
Books Book1, Book2;
```

可以使用 **typedef** 关键字来定义非结构类型，如下所示：

```
typedef long int *pint32;
 
pint32 x, y, z;
```

x, y 和 z 都是指向长整型 long int 的指针。