## 1、num->arr（短除法）

答案逆序数处

```c++
#include <algorithm>  // reverse()
#include <iostream>
#include <vector>
using namespace std;

vector<int> num_to_arr(int num) {
    vector<int> arr;
    while (num != 0) {
        arr.push_back(num % 10);
        num /= 10;
    }
    // 数组是逆向的
    reverse(arr.begin(), arr.end());
    return arr;
}

int main() {
    int num = 12345;
    vector<int> arr = num_to_arr(num);

    for (int a : arr) {
        cout << a << " ";
    }  // 1 2 3 4 5
    return 0;
}
```

## 2、arr->num

```c++
#include <iostream>
#include <vector>

using namespace std;

int array_to_num(vector<int> &arr) {
    int num = 0;
    int weight = 1;
    for (int i = arr.size() - 1; i >= 0; i--) {
        num += arr[i] * weight;
        weight *= 10;
    }
    return num;
}

int main() {
    vector<int> arr = {1, 2, 3, 4, 5};
    int num = array_to_num(arr);
    cout << num << endl;  // 12345
    return 0;
}
```

## 