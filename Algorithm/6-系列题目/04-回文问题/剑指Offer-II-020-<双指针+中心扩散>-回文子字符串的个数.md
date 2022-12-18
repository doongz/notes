题目：[剑指 Offer II 020. 回文子字符串的个数](https://leetcode.cn/problems/a7VOhD/)

给定一个字符串 `s` ，请计算这个字符串中有多少个回文子字符串。

具有不同开始位置或结束位置的子串，即使是由相同的字符组成，也会被视作不同的子串。

```
示例 1：

输入：s = "abc"
输出：3
解释：三个回文子串: "a", "b", "c"

示例 2：

输入：s = "aaa"
输出：6
解释：6个回文子串: "a", "a", "a", "aa", "aa", "aaa"
```

**提示：**

- `1 <= s.length <= 1000`
- `s` 由小写英文字母组成

注意：本题与主站 647 题相同：https://leetcode-cn.com/problems/palindromic-substrings/ 



---

```c++
class Solution {
public:
    string str;
    int n;

    int mid(int i) {
        int res = 0;
        int l = i;
        int r = i;
        while (l >= 0 && r < n) {
            if (str[l] == str[r]) {
                res++;
            } else {
                break;
            }
            l--;
            r++;
        }
        return res;
    }

    int gap(int i) {  // i下标后的间隙
        int res = 0;
        int l = i;
        int r = i + 1;
        while (l >= 0 && r < n) {
            if (str[l] == str[r]) {
                res++;
            } else {
                break;
            }
            l--;
            r++;
        }
        return res;
    }

    int countSubstrings(string s) {
        str = s;
        n = s.size();
        int ans = 0;
        for (int i = 0; i < n; i++) {
            ans += mid(i);  // 从中心点扩散
        }
        for (int i = 0; i < n - 1; i++) {
            ans += gap(i);  // 从间隙扩散
        }
        return ans;
    }
};
```

时间复杂度：O(n)
