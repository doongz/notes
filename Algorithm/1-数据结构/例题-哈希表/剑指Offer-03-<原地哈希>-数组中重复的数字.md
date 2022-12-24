题目：[剑指 Offer 03. 数组中重复的数字](https://leetcode.cn/problems/shu-zu-zhong-zhong-fu-de-shu-zi-lcof/)

找出数组中重复的数字。

在一个长度为 n 的数组 nums 里的所有数字都在 0～n-1 的范围内。数组中某些数字是重复的，但不知道有几个数字重复了，也不知道每个数字重复了几次。请找出数组中任意一个重复的数字。

**示例 1：**

```
输入：
[2, 3, 1, 0, 2, 5, 3]
输出：2 或 3 
```

**限制：**

```
2 <= n <= 100000
```

---

## 哈希表

使用哈希表的空间复杂度为 O(n)

```cpp
class Solution {
public:
    int findRepeatNumber(vector<int>& nums) {
        unordered_set<int> mem;
        for (int num : nums) {
            if (mem.count(num)) return num;
            mem.insert(num);
        }
        return -1;
    }
};
```

## 原地哈希

题目说明尚未被充分使用，即 `在一个长度为 n 的数组 nums 里的所有数字都在 0 ~ n-1 的范围内` 。 此说明含义：数组元素的 **索引** 和 **值** 是 **一对多** 的关系。

因此，可遍历数组并通过交换操作，使元素的 **索引** 与 **值** 一一对应（即 nums[i] = i）。因而，就能通过索引映射对应的值，起到与字典等价的作用。

![Picture0.png](../../img/1618146573-bOieFQ-Picture0.png)

遍历中，第一次遇到数字 x 时，将其交换至索引 x 处；而当第二次遇到数字 x 时，一定有 nums[x] = x ，此时即可得到一组重复数字。

##### 算法流程：

1. 遍历数组 nums ，设索引初始值为 i = 0:
   1. **若 nums[i] = i：** 说明此数字已在对应索引位置，无需交换，因此跳过；
   2. **若 nums[nums[i]] = nums[i]：** 代表索引 nums[i] 处和索引 i 处的元素值都为 nums[i]，即找到一组重复值，返回此值 nums[i]；
   3. **否则：** 交换索引为 i 和 nums[i] 的元素值，将此数字交换至对应索引位置。
2. 若遍历完毕尚未返回，则返回 -1。

复杂度分析：

- 时间复杂度 O(N)： 遍历数组使用 O(N)，每轮遍历的判断和交换操作使用 O(1)。
- 空间复杂度 O(1)： 使用常数复杂度的额外空间。

```cpp
class Solution {
public:
    int findRepeatNumber(vector<int>& nums) {
        int i = 0;
        while(i < nums.size()) {
            if(nums[i] == i) { // 如果已经放在对应位置上，就检查下个坐标 i
                i++;
                continue;
            } else { // 没有放在对应位置上，此时 nums[i] != i
                if (nums[nums[i]] == nums[i])
                    // nums[i] = a, a != i, 但是 nums[a] == nums[i]
                    // 一对多了就直接返回多的那个数
                    return nums[i];
                else if (nums[nums[i]] != nums[i]) {
                    // nums[i] = a, num[num[ i ] ]=num[ a ]=b, a!=b
                    // 交换后, num[ i ]=b, num[num[i]]=num[a]=a
                    // 这时候下标 a 对应的元素也是a
                    swap(nums[i],nums[nums[i]]);
                }
            }
        }
        return -1;
    }
};
```

nums[nums[i]], nums[i] = nums[i], nums[nums[i]]，为什么这里的交换可以让元素的 索引 与 值 相等。

下面供大家方便看出来（因为我看了好久才反应过来）：

记num[ i ] =a，num[num[ i ] ]=num[ a ]=b,那么 交换后，num[ i ]=b, num[num[i]]=num[a]=a，这时候下标 a 对应的元素也是a，达到目的
