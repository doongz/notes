题目：[剑指 Offer 38. 字符串的排列](https://leetcode.cn/problems/zi-fu-chuan-de-pai-lie-lcof/)

输入一个字符串，打印出该字符串中字符的所有排列。

你可以以任意顺序返回这个字符串数组，但里面不能有重复元素。

**示例:**

```
输入：s = "abc"
输出：["abc","acb","bac","bca","cab","cba"]
```

**限制：**

```
1 <= s 的长度 <= 8
```

---

结果中没有重复的原因在于，每层的这些递归不会重复使用 char

```cpp
class Solution {
public:
    int arr[26];
    int n;
    vector<string> ans;

    // cur 为当前补充的第 cur 位
    void dfs(int cur, string &path) {
        if (cur == n) {
            ans.push_back(path);
            return;
        }
        // 结果中没有重复的原因在这，每层的这些递归不会重复使用 char
        for (int i = 0; i < 26; i++) {
            if (arr[i] > 0) {
                arr[i]--;
                path += i + 'a';
                dfs(cur + 1, path);
                path.pop_back();
                arr[i]++;
            }
        }
    }

    vector<string> permutation(string s) {
        n = s.size();
        memset(arr, 0, sizeof(int) * 26);
        for (char c : s) {
            arr[c - 'a']++;
        }
        string path = "";
        dfs(0, path);
        return ans;
    }
};
```

