题目：[剑指 Offer 45. 把数组排成最小的数](https://leetcode.cn/problems/ba-shu-zu-pai-cheng-zui-xiao-de-shu-lcof/)

这里说的排列大小比较和字符串大小有点区别，比如 3 和 30，明显 30 排在前面比较好

所以我们要重构比较，我们组合 s1 和 s2 ，如果 s1 + s2 > s2 + s1，那么 s1 > s2

```c++
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