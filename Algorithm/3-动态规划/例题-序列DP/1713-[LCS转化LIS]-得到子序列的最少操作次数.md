题目：[1713. 得到子序列的最少操作次数](https://leetcode-cn.com/problems/minimum-operations-to-make-a-subsequence/)

## 方法：LCS 问题转化为 LIS 问题

### 思路历程

看完题目，答案显然是，先求出两个数组的最大公共子序列的长度 len，最后 target.size() - len

但是两个数组的最长都为 10^5，上述方法的时间复杂度为 O(nm)，显然会超时

那么，看到另一个条件： `target` 包含若干 **互不相同** 的整数

引导我们要将 **LCS 问题转化为 LIS 问题**，把时间复杂度 O(nm) 降至 O(nlogn)

声明：**LCS 转化为 LIS 问题的先决条件是，其中一个数组内的元素「不重复」**，例如 target 数组

还有个事实要明确：**「下标上升」意味着「顺序排布」，「顺序排布」意味着「下标上升」**，这是可以进行转化的理论基础

### 如何转化

**1. 预处理**：找出 arr 中且「同时存在」于 target 中的元素，将这些「同时存在」元素在「target 中的下标」，按照「arr 的顺序」缓存下来

例如：

```
target = [6,4,8,1,3,2]
arr = [4,7,6,2,3,8,6,1]
index_list = [1,0,5,4,2,0,3]
```

```c++
unordered_map<int, int> valIdx_map;
for (int i = 0; i < n; i++) {
    valIdx_map[target[i]] = i;
}
vector<int> index_list;
for (int num : arr) {
    if (valIdx_map.count(num)) {
        // cout << num << " " << "idx in target:" << valIdx_map[num] << endl;
        index_list.push_back(valIdx_map[num]);
    }
}
```

**2. 将 LCS 转化为 LIS 问题**

首先看下 index_list 内的这些元素具备什么性质：

- 里面存储的元素是 target 的下标
- 是按照在 arr 中的顺序构成的
- 根据 target 的下标，检索出的数，是属于 target 和 arr 公共的

在这样一个 index_list 中求出「最长上升子序列」，这个 LIS 具备什么性质：

- 「同时」满足了在 target 和 arr 中按照「顺序」排布，**「下标上升」意味着「顺序排布」，「顺序排布」意味着「下标上升」**
- 其中的元素，「同时」存在于 target 和 arr 中，也就是公共的

这样的一个序列，对于 index_list 是「最长上升子序列」，对于 target 和 arr 就是「最长公共子序列」

求解的过程，就是将 LCS 问题转化为 LIS 问题

> 问：为什么其中一个数组内的元素「不重复」，这样的转换方式才能生效呢？
>
> - 如果 target 数组中某个元素重复出现，应该选择其中的哪个下标来构成最终的那个最长上升子序列」，那么就又得一个个判断这些重复值O(n)，整体的时间复杂度退化为 O(nm)，这样的转换方式又有什么意义
>
> - 如果 target 数组中所有元素都是「不重复」，直接就可选中在target唯一的公共元素 O(1)，嵌入到LCS的O(nlogn)的求解过程中，整体的时间复杂度优化为O(nlogn)

时间复杂度：`O(nlogn)`

空间复杂度：`O(n)`

```c++
class Solution {
public:
    int minOperations(vector<int>& target, vector<int>& arr) {
        int n = target.size();
        int m = arr.size();

        unordered_map<int, int> valIdx_map;
        for (int i = 0; i < n; i++) {
            valIdx_map[target[i]] = i;
        }
        vector<int> index_list;
        for (int num : arr) {
            if (valIdx_map.count(num)) {
                index_list.push_back(valIdx_map[num]);
            }
        }
        if (index_list.empty()) {  // 没有公共子序列
            return n;
        }

        vector<int> tail;
        tail.push_back(index_list[0]);
        for (int i = 1; i < index_list.size(); i++) {
            int cur = index_list[i];
            int end = *tail.rbegin();
            if (cur > end) {
                tail.push_back(cur);
            } else {
                auto it = lower_bound(tail.begin(), tail.end(), cur);
                *it = cur;
            }
        }
        return n - tail.size();
    }
};
```

