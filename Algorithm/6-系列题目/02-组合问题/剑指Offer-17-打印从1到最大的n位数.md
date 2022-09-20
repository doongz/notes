题目：[剑指 Offer 17. 打印从1到最大的n位数](https://leetcode.cn/problems/da-yin-cong-1dao-zui-da-de-nwei-shu-lcof/)

## 方法一：绝对不可以的解法！

面试的时候千万别这么写

- 时间复杂度：O(10 ^ n)

```c++
class Solution {
public:
    vector<int> printNumbers(int n) {
        if(n <= 0) return vector<int>(0);
        vector<int> res;
        int num = 1;
        for(int i=0; i<n; ++i)
            num *= 10; // 比如 n=3，num就是1000
        for(int i=1; i<num; ++i) res.push_back(i);
        return res;
    }
};
```

## 思路二：全排列解法（大数法）

在数字很大的情况下，哪怕long类型也无法承载，那必须要用字符串保存。

```c++
class Solution {
public:
    vector<int> ans;

    void dfs(string &path, int now, int depth) {
        if (now == depth) {
            ans.push_back(stoi(path));
            return;
        }
        for (int i = 0; i < 10; i++) {
            if (now == 0 && i == 0) continue;
            path.push_back(48 + i);
            dfs(path, now + 1, depth);
            path.pop_back();
        }
    }

    vector<int> printNumbers(int n) {
        for (int d = 1; d <= n; d++) {
            string path = "";
            dfs(path, 0, d);
        }

        return ans;
    }
};
```