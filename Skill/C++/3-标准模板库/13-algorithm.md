# algorithm

来源：[http://c.biancheng.net/stl/](http://c.biancheng.net/stl/)

## 比较

### 1、max()

```c++
int res = max(5, 4);
cout << res << endl; // 5
```

## 一、排序

| 函数名                                                     | 用法                                                         |
| ---------------------------------------------------------- | ------------------------------------------------------------ |
| sort (first, last)                                         | 对容器或普通数组中 [first, last) 范围内的元素进行排序，默认进行升序排序。 |
| stable_sort (first, last)                                  | 和 sort() 函数功能相似，不同之处在于，对于 [first, last) 范围内值相同的元素，该函数不会改变它们的相对位置。 |
| partial_sort (first, middle, last)                         | 从 [first,last) 范围内，筛选出 muddle-first 个最小的元素并排序存放在 [first，middle) 区间中。 |
| partial_sort_copy (first, last, result_first, result_last) | 从 [first, last) 范围内筛选出 result_last-result_first 个元素排序并存储到 [result_first, result_last) 指定的范围中。 |
| is_sorted (first, last)                                    | 检测 [first, last) 范围内是否已经排好序，默认检测是否按升序排序。 |
| is_sorted_until (first, last)                              | 和 is_sorted() 函数功能类似，唯一的区别在于，如果 [first, last) 范围的元素没有排好序，则该函数会返回一个指向首个不遵循排序规则的元素的迭代器。 |
| void nth_element (first, nth, last)                        | 找到 [first, last) 范围内按照排序规则（默认按照升序排序）应该位于第 nth 个位置处的元素，并将其放置到此位置。同时使该位置左侧的所有元素都比其存放的元素小，该位置右侧的所有元素都比其存放的元素大。 |

### 1、sort()

- sort() 函数是基于快速排序实现的，默认由小到大
- 只对 array、vector、deque 这 3 个容器提供支持
- 对于指定区域内值相等的元素，sort() 函数无法保证它们的相对位置不发生改变

```c++
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

// 以普通函数的方式实现自定义排序规则，< 大的在前
bool cmp1(int i, int j) {
    return (i < j);
}

// （推荐）以函数对象的方式实现自定义排序规则，> 大的在前
class cmp2 {
public:
    // 重载 operator
    bool operator()(int i, int j) {
        return (i > j);
    }
};

void show(vector<int> vec) {
    for (int i = 0; i < vec.size(); i++) {
        cout << vec[i] << " ";
    }
    cout << endl;
}

int main() {
    vector<int> vec{5, 2, 3, 4, 1};

    sort(vec.begin(), vec.end());        // 1 2 3 4 5
    sort(vec.begin(), vec.begin() + 3);  // 2 3 5 4 1

    sort(vec.begin(), vec.end(), greater<int>());  // 5 4 3 2 1
    sort(vec.begin(), vec.end(), cmp1());          // 5 4 3 2 1
    sort(vec.begin(), vec.end(), cmp2());          // 5 4 3 2 1

    show(vec);
    return 0;
}
```

### 2、stable_sort()

stable_sort() 函数是基于归并排序实现的，完全可看作是 sort() 函数的升级版，语法格式、使用也相同

- stable_sort() 在功能上除了可以实现排序，还可以保证不改变相等元素的相对位置。

有些场景是需要保证相等元素的相对位置的。例如对于一个保存某种事务（比如银行账户）的容器，在处理这些事务之前，为了能够有序更新这些账户，需要按照账号对它们进行排序。而这时就很有可能出现相等的账号（即同一账号在某段时间做多次的存取钱操作），它们的相对顺序意味着添加到容器的时间顺序，此顺序不能修改，否则很可能出现账户透支的情况。

### 3、paritial_sort()

场景：有一个存有 100 万个元素的容器，但只想从中提取出值最小的 10 个元素，该如何实现呢？如果用 sort() 或者 stable_sort() 排序函数，即通过对容器中存储的 100 万个元素进行排序，再筛选出最小的 10 个元素，这种实现方式的效率是非常低的。

paritial_sort() 函数可以从指定区域中提取出部分数据，并对它们进行排序。 只适用于 array、vector、deque 这 3 个容器

语法格式为：

```c++
//按照默认的升序排序规则，对 [first, last) 范围的数据进行筛选并排序
void partial_sort (RandomAccessIterator first,
                   RandomAccessIterator middle,
                   RandomAccessIterator last);
//按照 comp 排序规则，对 [first, last) 范围的数据进行筛选并排序
void partial_sort (RandomAccessIterator first,
                   RandomAccessIterator middle,
                   RandomAccessIterator last,
                   Compare comp);
```

partial_sort() 函数会以**交换元素存储位置的方式实现部分排序的**。将 [first, last) 范围内最小（或最大）的 middle-first 个元素移动到 [first, middle) 区域中，并对这部分元素做升序（或降序）排序。 [middle, last)范围内的元素不保证是原有的顺序

```c++
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

// 以普通函数的方式实现自定义排序规则，< 大的在前
bool cmp1(int i, int j) {
    return (i < j);
}

// （推荐）以函数对象的方式实现自定义排序规则，> 大的在前
class cmp2 {
public:
    // 重载 operator
    bool operator()(int i, int j) {
        return (i > j);
    }
};

void show(vector<int> vec) {
    for (int i = 0; i < vec.size(); i++) {
        cout << vec[i] << " ";
    }
    cout << endl;
}

int main() {
    vector<int> vec{3, 2, 5, 4, 1, 6, 9, 7};

    // 默认升序，最小的 4 个元素移动到开头并排好序
    partial_sort(vec.begin(), vec.begin() + 4, vec.end());  // 1 2 3 4 5 6 9 7

    // 指定降序，最小的 4 个元素移动到开头并排好序
    partial_sort(vec.begin(), vec.begin() + 4, vec.end(), greater<int>());  // 9 7 6 5 1 2 3 4

    // 指定排序方式
    partial_sort(vec.begin(), vec.begin() + 4, vec.end(), cmp2());  // 9 7 6 5 1 2 3 4

    show(vec);
    return 0;
}
```

### 4、partial_sort_copy()

partial_sort_copy() 函数的功能和 partial_sort() 类似，唯一的区别在于，**不会对原有数据做任何变动，而是先将选定的部分元素拷贝到另外指定的数组或容器中，再对这部分元素进行排序。**

语法格式:

```c++
//默认以升序规则进行部分排序
RandomAccessIterator partial_sort_copy (
                       InputIterator first,
                       InputIterator last,
                       RandomAccessIterator result_first,
                       RandomAccessIterator result_last);
//以 comp 规则进行部分排序
RandomAccessIterator partial_sort_copy (
                       InputIterator first,
                       InputIterator last,
                       RandomAccessIterator result_first,
                       RandomAccessIterator result_last,
                       Compare comp);
```

partial_sort_copy() 函数会将 [first, last) 范围内最小（或最大）的 result_last-result_first 个元素复制到 [result_first, result_last) 区域中，并对该区域的元素做升序（或降序）排序。

```c++
vector<int> vec{3, 2, 5, 4, 1, 6, 9, 7};
vector<int> res(5, 0);

partial_sort_copy(vec.begin(), vec.end(), res.begin(), res.end());  // 1 2 3 4 5
partial_sort_copy(vec.begin(), vec.end(), res, res + 5);            // 1 2 3 4 5
```

### 5、nth_elelment()

th_element() 函数的功能：

当采用默认的升序排序规则（std::less<T>）时，该函数可以从某个序列中找到第 n 小的元素 K，并将 K 移动到序列中第 n 的位置处。此时，所有位于 K 之前的元素都比 K 小，所有位于 K 之后的元素都比 K 大。

```c++
//排序规则采用默认的升序排序
void nth_element (RandomAccessIterator first,
                  RandomAccessIterator nth,
                  RandomAccessIterator last);
//排序规则为自定义的 comp 排序规则
void nth_element (RandomAccessIterator first,
                  RandomAccessIterator nth,
                  RandomAccessIterator last,
                  Compare comp);
```

```c++
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> vec{3, 1, 2, 5, 4};
    // 第三小的放在第三位置上，前面的都比它小，后面的都比它大
    nth_element(vec.begin(), vec.begin() + 2, vec.end());  // 2 1 3 4 5
    return 0;
}
```

### 6、is_sorted()

is_sorted() 函数用于判断某个序列是否为有序序列。

当程序中涉及排序操作时，应该为其包裹一层判断语句 `if is_sorted()` 避免执行一些不必要的排序操作

语法格式:

```c++
//判断 [first, last) 区域内的数据是否符合 std::less<T> 排序规则，即是否为升序序列
bool is_sorted (ForwardIterator first, ForwardIterator last);
//判断 [first, last) 区域内的数据是否符合 comp 排序规则  
bool is_sorted (ForwardIterator first, ForwardIterator last, Compare comp);
```

```c++
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

void show(vector<int> vec) {
    for (int i = 0; i < vec.size(); i++) {
        cout << vec[i] << " ";
    }
    cout << endl;
}

// （推荐）以函数对象的方式实现自定义排序规则，> 大的在前
class cmp {
public:
    // 重载 operator
    bool operator()(int i, int j) {
        return (i > j);
    }
};

int main() {
    vector<int> vec{3, 1, 2, 5, 4};

    if (!is_sorted(vec.begin(), vec.end())) {
        cout << "not small -> big" << endl;
        sort(vec.begin(), vec.end());
    }
    show(vec);  // 1 2 3 4 5

    if (!is_sorted(vec.begin(), vec.end(), cmp())) {
        cout << "not big -> small" << endl;
        sort(vec.begin(), vec.end(), cmp());
    }
    show(vec);  // 5 4 3 2 1

    return 0;
}
```

### 7、merge()

merge() 函数用于**将 2 个有序序列合并为 1 个有序序列**，前提是这 2 个有序序列的排序规则相同（要么都是升序，要么都是降序）。并且最终借助该函数获得的新有序序列，其排序规则也和这 2 个有序序列相同。

```c++
//以默认的升序排序作为排序规则
OutputIterator merge (InputIterator1 first1, InputIterator1 last1,
                      InputIterator2 first2, InputIterator2 last2,
                      OutputIterator result);
//以自定义的 comp 规则作为排序规则
OutputIterator merge (InputIterator1 first1, InputIterator1 last1,
                      InputIterator2 first2, InputIterator2 last2,
                      OutputIterator result, Compare comp);
```

```c++
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

void show(vector<int> vec) {
    for (int i = 0; i < vec.size(); i++) {
        cout << vec[i] << " ";
    }
    cout << endl;
}

int main() {
    vector<int> vec1{3, 5, 7, 9};
    vector<int> vec2{1, 2, 4, 6, 8};
    vector<int> res(9);

    merge(vec1.begin(), vec1.end(), vec2.begin(), vec2.end(), res.begin());
    show(res);  // 1 2 3 4 5 6 7 8 9

    return 0;
}
```

### 8、inplace_merge()

当 2 个有序序列存储在同一个数组或容器中时，inplace_merge() 函数将它们合并为 1 个有序序列

```c++
vector<int> vec{3, 5, 7, 9, 1, 2, 4, 6, 8};

inplace_merge(vec, vec + 4, vec.end());
// 1 2 3 4 5 6 7 8 9
```

### 9、next_permutation()

在容器内所有元素的排列组合中，排序为最小的一个，即升序的方式生成排列

```c++
vector<int> vec{5, 3, 1, 2, 4};

while (next_permutation(vec.begin(), vec.end())) {
}
for (int i = 0; i < vec.size(); i++) {
    cout << vec[i] << " ";
}
// 1 2 3 4 5
```

### 10、prev_permutation()

在容器内所有元素的排列组合中，排序为最大的一个，即降序的方式生成排列

```c++
vector<int> vec{5, 3, 1, 2, 4};

while (prev_permutation(vec.begin(), vec.end())) {
}
for (int i = 0; i < vec.size(); i++) {
    cout << vec[i] << " ";
}
// 5 4 3 2 1
```



## 二、查找

在无序序列中查

### 1、find()

find() 函数用于在指定范围内查找和目标元素值相等的第一个元素。

该函数会返回一个输入迭代器，当 find() 函数查找成功时，其指向的是在 [first, last) 区域内查找到的第一个目标元素；如果查找失败，则该迭代器的指向和 last 相同。

find() 函数的底层实现，其实就是用`==`运算符将 val 和 [first, last) 区域内的元素逐个进行比对。这也就意味着，[first, last) 区域内的元素必须支持`==`运算符

```c++
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> vec{1, 2, 2, 2, 3};
    auto it = find(vec.begin(), vec.end(), 2);
    if (it != vec.end()) {
        cout << "find it" << endl;
    } else {
        cout << "not find" << endl;
    }
    // find it

    return 0;
}
```

### 2、find_if()

find_if() 函数允许自定义查找规则，形参为返回值类型为 bool 的函数

find_if() 函数会根据指定的查找规则，在指定区域内查找第一个符合该函数要求（使函数返回 true）的元素。

```c++
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

// 以函数对象的形式定义一个 find_if() 函数的查找规则
class cmp {
public:
    bool operator()(const int& i) {
        return ((i % 2) == 0);
    }
};

int main() {
    vector<int> vec{1, 2, 2, 2, 3};

    vector<int>::iterator it = find_if(vec.begin(), vec.end(), cmp());
    cout << *it << endl;  // 2

    return 0;
}
```

### 3、find_if_not()

find_if_not() 函数则用于查找第一个不符合谓词函数规则的元素

```c++
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

// 以函数对象的形式定义一个 find_if() 函数的查找规则
class cmp {
public:
    bool operator()(const int& i) {
        return ((i % 2) == 0);
    }
};

int main() {
    vector<int> vec{1, 2, 2, 2, 3};

    vector<int>::iterator it = find_if_not(vec.begin(), vec.end(), cmp());
    cout << *it << endl;  // 1

    return 0;
}
```

### 4、find_end()

find_end() 函数在序列 A 中查找序列 B 最后一次出现的位置 

```c++
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> vec{1, 2, 3, 2, 3};
    vector<int> v{2, 3};
    vector<int>::iterator it = find_end(vec.begin(), vec.end(), v.begin(), v.end());
    if (it != vec.end()) {
        cout << "idx: " << it - vec.begin() << endl;
    }
    // idx: 3

    return 0;
}
```

### 5、find_first_of()

find_first_of() 函数在 A 序列中查找和 B 序列中任意元素相匹配的第一个元素

```c++
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

//以函数对象的形式定义一个 find_first_of() 函数的匹配规则
class cmp {
public:
    bool operator()(const int& c1, const int& c2) {
        return (c2 % c1 == 0);
    }
};
int main() {
    vector<int> vec{5, 7, 3, 9};
    int inter[] = {4, 6, 8};
    //调用第二种语法格式，找到 vec 容器中任一元素有 c2%c1=0 关系的第一个元素
    vector<int>::iterator iter = find_first_of(vec.begin(), vec.end(), inter, inter + 3, cmp());
    if (iter != vec.end()) {
        cout << *iter << endl;
    }
    // 3

    return 0;
}
```

### 6、adjacent_find()

adjacent_find() 函数用于在指定范围内查找连续 2 个满足规则的元素，默认两个相等的元素

```c++
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

class cmp {
public:
    bool operator()(const int& _Left, const int& _Right) {
        return (_Left != _Right);
    }
};
int main() {
    vector<int> vec{1, 2, 2, 3};
    vector<int>::iterator it = adjacent_find(vec.begin(), vec.end());

    if (it != vec.end()) {
        cout << "idx: " << it - vec.begin() << endl;
        cout << *it << endl;
    }
    // idx: 1
    // 2

    auto res = adjacent_find(vec.begin(), vec.end(), cmp());
    if (res != vec.end()) {
        cout << "idx: " << res - vec.begin() << endl;
        cout << *res << endl;
    }
    // idx: 0
    // 1

    return 0;
}
```

### 7、search()

search() 函数查找序列 B 在序列 A 中第一次出现的位置

```c++
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> vec{1, 2, 3, 2, 3};
    vector<int> v{2, 3};
    vector<int>::iterator it = search(vec.begin(), vec.end(), v.begin(), v.end());
    if (it != vec.end()) {
        cout << "idx: " << it - vec.begin() << endl;
    }
    // idx: 1

    return 0;
}
```

### 8、search_n()

search_n() 函数功能与search() 函数类似，但只能查找包含多个相同元素的子序列。

```c++
vector<int> vec{1, 2, 3, 2, 2};
vector<int> v{2, 2};
vector<int>::iterator it = search_n(vec.begin(), vec.end(), v.begin(), v.end());
if (it != vec.end()) {
    cout << "idx: " << it - vec.begin() << endl;
}
// idx: 3
```

## 四、二分查找

在有序序列中查

### 1、lower_bound()

lower_bound() 函数用于在指定区域内查找 **等于或大于目标值的第一个元素**

```c++
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int arr[5] = {1, 2, 3, 3, 4};

    int *p = lower_bound(arr, arr + 5, 3);
    cout << "idx: " << p - arr << " val: " << *p << endl;
    // idx: 2 val: 3

    vector<int> vec1 = {1, 2, 3, 3, 4};
    auto res1 = lower_bound(vec1.begin(), vec1.end(), 3);
    cout << "idx: " << res1 - vec1.begin() << " val: " << *res1 << endl;
    // idx: 2 val: 3

    vector<int> vec2 = {1, 2, 4, 4, 4};
    auto res2 = lower_bound(vec2.begin(), vec2.end(), 3);
    cout << "idx: " << res2 - vec2.begin() << " val: " << *res2 << endl;
    // idx: 2 val: 4
    return 0;
}
```

### 2、upper_bound()

upper_bound() 函数用于在指定范围内查找 **大于目标值的第一个元素**

```c++
int arr[5] = {1, 2, 3, 3, 4};

int *p = upper_bound(arr, arr + 5, 3);
cout << "idx: " << p - arr << " val: " << *p << endl;
// idx: 4 val: 4

vector<int> vec1 = {1, 2, 3, 3, 4};
auto res1 = upper_bound(vec1.begin(), vec1.end(), 3);
cout << "idx: " << res1 - vec1.begin() << " val: " << *res1 << endl;
// idx: 4 val: 4

vector<int> vec2 = {1, 2, 4, 4, 4};
auto res2 = upper_bound(vec2.begin(), vec2.end(), 3);
cout << "idx: " << res2 - vec2.begin() << " val: " << *res2 << endl;
// idx: 2 val: 4
```

### 3、equel_range()

equel_range() 函数用于在指定范围内查找 **等于目标值的所有元素**

```c++
int arr[6] = {1, 2, 3, 3, 3, 4};
pair<int*, int*> range1 = equal_range(arr, arr + 6, 3);
cout << "first: " << range1.first - arr
        << " second: " << range1.second - arr << endl;
// first: 2 second: 5

vector<int> vec = {1, 2, 3, 3, 3, 4};
pair<vector<int>::iterator, vector<int>::iterator> range2;
range2 = equal_range(vec.begin(), vec.end(), 3);
cout << "first: " << range2.first - vec.begin()
        << " second: " << range2.second - vec.begin() << endl;
// first: 2 second: 5
```

### 4、binary_search()

binary_search() 用于查找指定区域内是否包含某个目标元素

```c++
vector<int> vec = {1, 2, 3, 3, 3, 4};
bool res1 = binary_search(vec.begin(), vec.end(), 3);
cout << res1 << endl;  // 1

bool res2 = binary_search(vec.begin(), vec.end(), 5);
cout << res2 << endl;  // 0
```

## 五、分组

### 1、partition()

partition() 函数可根据用户自定义的筛选规则，重新排列指定区域内存储的数据，使其分为 2 组，第一组为符合筛选条件的数据，另一组为不符合筛选条件的数据。其实会把数据放到原处，前面一半满足规则，后面一半不满足，也不关心分组后各个元素具体的存储位置。

返回第二组的第一个边界元素

```c++
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

class cmp {
public:
    bool operator()(const int& i) {
        return (i % 2 == 0);
    }
};

int main() {
    vector<int> vec{1, 2, 3, 4, 5, 6, 7, 8, 9};

    //以 cmp 规则，对 vec  容器中的数据进行分组
    auto bound = partition(vec.begin(), vec.end(), cmp());
    for (auto it = vec.begin(); it != vec.end(); ++it) {
        cout << *it << " ";
    }                                // 8 2 6 4 5 3 7 1 9
    cout << "\nbound = " << *bound;  // bound = 5
    return 0;
}
```

### 2、stable_partition()

stable_partition() 函数可以保证对指定区域内数据完成分组的同时，不改变各组内元素的相对位置

返回第二组的第一个边界元素

```c++
vector<int> vec{1, 2, 3, 4, 5, 6, 7, 8, 9};

//以 cmp 规则，对 vec  容器中的数据进行分组
auto bound = stable_partition(vec.begin(), vec.end(), cmp());
for (auto it = vec.begin(); it != vec.end(); ++it) {
    cout << *it << " ";
}
cout << endl;  // 2 4 6 8 1 3 5 7 9
for (auto it = vec.begin(); it != bound; ++it) {
    cout << *it << " ";
}  // 2 4 6 8
```

### 3、partition_copy()

partition_copy() 函数

- 按照某个筛选规则对指定区域内的数据进行“分组”
- 分组后不会改变各个元素的相对位置
- 不会对原序列做修改，以复制的方式到其它的指定位置

```c++
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

class cmp {
public:
    bool operator()(const int &i) {
        return (i % 2 == 0);
    }
};

int main() {
    vector<int> vec{1, 2, 3, 4, 5, 6, 7, 8, 9};
    int a[10] = {0};
    int b[10] = {0};

    pair<int *, int *> res = partition_copy(vec.begin(), vec.end(), a, b, cmp());
    for (int *p = a; p < res.first; p++) {
        cout << *p << " ";
    }
    cout << endl;  // 2 4 6 8

    for (int *p = b; p < res.second; p++) {
        cout << *p << " ";
    }  // 1 3 5 7 9

    return 0;
}
```

### 4、partition_point()

partition_point() 函数在已分好组的数据中找到分界位置

## 六、判断

### 1、all_of()

序列中的所有元素「都满足条件时」，返回自定义的 true 结果，否则返回 false 结果

```c++
vector<int> ages{6, 7, 8, 9};
int max_age = 10;

// 判断向量中全部都小于 10
string res;
res = (all_of(ages.begin(), ages.end(), [max_age](int age) { return age < max_age; }) ? "Yes" : "No");
cout << res << endl;  // Yes
```

### 2、any_of()

序列中的元素「有一个满足条件时」，返回自定义的 true 结果，否则返回 false 结果

```c++
vector<int> ages{6, 7, 8, 9};
int max_age = 7;

// 判断向量中有一个小于 7
string res;
res = (any_of(ages.begin(), ages.end(), [max_age](int age) { return age < max_age; }) ? "Yes" : "No");
cout << res << endl;  // Yes
```

### 3、none_of()

序列中的所有元素「都不满足条件时」，返回自定义的 true 结果，否则返回 false 结果

```c++
vector<int> ages{6, 7, 8, 9};
int min_age = 5;

// 判断向量中没有一个小于5
string res;
res = (none_of(ages.begin(), ages.end(), [min_age](int age) { return age < min_age; }) ? "Yes" : "No");
cout << res << endl;  // Yes
```

### 4、equal()

equal() 比较两个序列是否相等，包括元素值和元素排序，推荐使用接受 4 个参数的版本

```c++
vector<int> vec1 = {1, 2, 3, 4};
vector<int> vec2 = {2, 3, 4, 5};

cout << equal(vec1.begin(), vec1.end(), vec2.begin(), vec2.end()) << endl;          // 0
cout << equal(vec1.begin() + 1, vec1.end(), vec2.begin(), vec2.end() - 1) << endl;  // 1
cout << equal(vec1.begin() + 1, vec1.end(), vec2.begin()) << endl;                  // 1
```

### 5、is_permutation()

is_permutation() 比较两个序列是否相等，只检查元素值，不包含元素排序

```c++
vector<int> vec1{5, 3, 1, 2, 4};
vector<int> vec2{1, 2, 3, 4, 5};

bool res1 = is_permutation(vec1.begin(), vec1.end(), vec2.begin(), vec2.end());
bool res2 = equal(vec1.begin(), vec1.end(), vec2.begin(), vec2.end());
cout << res1 << endl;  // 1
cout << res2 << endl;  // 0
```

### 6、mismatch()

mismatch() 也可以判断两个序列是否匹配，而且如果不匹配，返回不匹配的位置

### 7、lexicographical_compare()

字符串字典许排序算法

```c++
vector<string> phrase1{"the", "tigers", "of", "wrath"};
vector<string> phrase2{"the", "horses", "of", "instruction"};
bool res = lexicographical_compare(begin(phrase1), end(phrase1),
                                    begin(phrase2), end(phrase2));
cout << res << endl;  // 0 因为 tigers 大于 horses
```

## 七、改变

### 1、unique()

unique() 算法可以在序列中原地移除重复的元素



### 2、replace()

新的值来替换和给定值相匹配的元素

