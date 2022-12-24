题目：[剑指 Offer 45. 把数组排成最小的数](https://leetcode.cn/problems/ba-shu-zu-pai-cheng-zui-xiao-de-shu-lcof/)

输入一个非负整数数组，把数组里所有数字拼接起来排成一个数，打印能拼接出的所有数字中最小的一个。

**示例 1:**

```
输入: [10,2]
输出: "102"
```

**示例 2:**

```
输入: [3,30,34,5,9]
输出: "3033459"
```

提示:

0 < nums.length <= 100

说明:

输出结果可能非常大，所以你需要返回一个字符串而不是整数
拼接起来的数字可能会有前导 0，最后结果不需要去掉前导 0



这里说的排列大小比较和字符串大小有点区别，比如 3 和 30，明显 30 排在前面比较好

所以我们要重构比较，我们组合 s1 和 s2 ，如果 s1 + s2 > s2 + s1，那么 s1 > s2

```cpp
class Solution {
public:
    string minNumber(vector<int> &nums) {
        vector<string> nums_str;
        for (int num : nums) {
            nums_str.push_back(to_string(num));
        }

        auto cmp = [&](const auto &a, const auto &b) {
            return a + b < b + a;
        };
        sort(nums_str.begin(), nums_str.end(), cmp);

        string ans = "";
        for (string &s : nums_str) {
            ans += s;
        }
        return ans;
    }
};
```