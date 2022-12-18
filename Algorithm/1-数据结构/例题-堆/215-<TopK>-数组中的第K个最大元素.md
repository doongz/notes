[215. 数组中的第K个最大元素](https://leetcode-cn.com/problems/kth-largest-element-in-an-array/)

给定整数数组 `nums` 和整数 `k`，请返回数组中第 `k` 个最大的元素。

请注意，你需要找的是数组排序后的第 `k` 个最大的元素，而不是第 `k` 个不同的元素。

你必须设计并实现时间复杂度为 `O(n)` 的算法解决此问题。

**示例 1:**

```
输入: [3,2,1,5,6,4], k = 2
输出: 5
```

**示例 2:**

```
输入: [3,2,3,1,2,4,5,5,6], k = 4
输出: 4
```

**提示：** 

- `1 <= k <= nums.length <= 105`
- `-104 <= nums[i] <= 104`

## 方法一：排序函数

时间复杂度：O(nlogn)，「快速排序」的时间复杂度

空间复杂度：O(logn)，「快速排序」的空间复杂度为递归调用栈的高度

执行用时：8 ms, 在所有 C++ 提交中击败了73.59%的用户

内存消耗：9.6 MB, 在所有 C++ 提交中击败了94.42%的用户

```c++
class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        sort(nums.begin(), nums.end(), greater<int>());
        return nums[k-1];
    }
};
```

## 方法二：堆

这里用小根堆实现

- 维持小根堆内的元素个数为 k 个
- 如果元素比堆顶元素大，移除堆顶，然后入堆
- 遍历完后，堆顶就是答案

时间复杂度：O(nlogk)

空间复杂度：O(k)

`k`远小于`n`，时间复杂度`O(nlogk)`趋近于`O(n)`，而空间复杂度`O(k)`则近似于`O(1)`

执行用时：8 ms, 在所有 C++ 提交中击败了73.59%的用户

内存消耗：15.1 MB, 在所有 C++ 提交中击败了5.03%的用户

```c++
class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        priority_queue<int, deque<int>, greater<int>> smallQ(nums.begin(), nums.begin() + k);
        for (int i = k; i < nums.size(); i++) {
            if (nums[i] > smallQ.top()) {
                smallQ.pop();
                smallQ.push(nums[i]);
            }
        }
        return smallQ.top();
    }
};
```

## 方法三、partition 减而治之

https://leetcode-cn.com/problems/kth-largest-element-in-an-array/solution/partitionfen-er-zhi-zhi-you-xian-dui-lie-java-dai-/
