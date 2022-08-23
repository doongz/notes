[140. 单词拆分 II](https://leetcode-cn.com/problems/word-break-ii/)

## 方法：记忆化搜索

观察「递归树」思考：

- 是否具备「最优子结构」，是
- 是否具备「重复子问题」，是

![](../doc/140.png)

偷懒，没分析复杂度

```c++
class Solution {
public:
    int sz;
    vector<vector<string>> memo;
    unordered_set<string> wordSet;

    vector<string> dfs(int cur, string& s) {
        if (cur == sz) return {""};  // 达到结尾，返回空字符串
        if (memo[cur].size() != 0) return memo[cur];

        vector<string> res;
        for (int end = cur; end < sz; end++) {
            string sub = s.substr(cur, end - cur + 1);  // 获取下个可能的字符
            if (wordSet.count(sub)) {
                vector<string> right = dfs(end + 1, s);  // 当前字符后面的所有路径
                for (string path : right) {
                    if (path == "") {  // 如果这个路径是空，说明到底了
                        res.push_back(sub);
                    } else {  // 每个路径头上 加上 当前的字符
                        res.push_back(sub + " " + path);
                    }
                }
            }
        }
        memo[cur] = res;
        return res;
    }

    vector<string> wordBreak(string s, vector<string>& wordDict) {
        sz = s.size();
        for (string word : wordDict) {
            wordSet.insert(word);
        }
        // memo[i]表示，以s[i]结尾的所有可能
        for (int i = 0; i < sz; i++) {
            memo.push_back({});
        }
        return dfs(0, s);
    }
};
```

