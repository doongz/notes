题目：[剑指 Offer 66. 构建乘积数组](https://leetcode.cn/problems/gou-jian-cheng-ji-shu-zu-lcof/)

给定一个数组 `A[0,1,…,n-1]`，请构建一个数组 `B[0,1,…,n-1]`，其中 `B[i]` 的值是数组 `A` 中除了下标 `i` 以外的元素的积, 即 `B[i]=A[0]×A[1]×…×A[i-1]×A[i+1]×…×A[n-1]`。不能使用除法。

**示例:**

```
输入: [1,2,3,4,5]
输出: [120,60,40,30,24]
```

**提示：**

- 所有元素乘积之和不会溢出 32 位整数
- `a.length <= 100000`

---

```cpp
class Solution {
public:
    vector<int> constructArr(vector<int>& a) {
        // 两个dp数组，分别维护 i 左侧、右侧的乘积和
        int n = a.size();
        vector<int> dp_l(n, 1); // dp_l[i] 表示 i 位置左边元素的乘积
        vector<int> dp_r(n, 1); // dp_r[i] 表示 i 位置右边元素的乘积
        for (int i = 1; i < n; i++) {
            dp_l[i] = dp_l[i-1] * a[i-1];
        }
        for (int i = n - 2; i >= 0; i--) {
            dp_r[i] = dp_r[i+1] * a[i+1];
        }
        
        vector<int> ans(n);
        for (int i = 0; i < n; i++) {
            ans[i] = dp_l[i] * dp_r[i];
        }
        return ans;
    }
};
```

