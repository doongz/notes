[212. 单词搜索 II](https://leetcode-cn.com/problems/word-search-ii/)

## 方法一：回溯

数据范围只有 12，且 words 中出现的单词长度不会超过 10，可以考虑使用「回溯算法」。

起始先将所有 words 出现的单词放到 Set 结构中，然后以 board 中的每个点作为起点进行爆搜（由于题目规定在一个单词中每个格子只能被使用一次，因此还需要一个 vis 数组来记录访问过的位置）：

- 如果当前爆搜到的字符串长度超过 10，直接剪枝；

- 如果当前搜索到的字符串在 Set 中，则添加到答案（同时了防止下一次再搜索到该字符串，需要将该字符串从 Set 中移除）

时间复杂度：`O(m*n*4^10)`，共有 m * n 个起点，每次能往 4 个方向搜索（不考虑重复搜索问题），且搜索的长度不会超过 10

空间复杂度：``O(words[i].length)``

执行用时：872 ms, 在所有 C++ 提交中击败了35.37%的用户

内存消耗：9.8 MB, 在所有 C++ 提交中击败了94.37%的用户

```c++
class Solution {
private:
    unordered_set<string> us;
    vector<vector<char>> board;
    vector<pair<int, int>> direction;
    int rows;
    int cols;
    bool visited[12][12];
    vector<string> ans;

public:
    vector<string> findWords(vector<vector<char>>& _board, vector<string>& words) {
        board = _board;
        direction = {{1, 0}, {0, 1}, {-1, 0}, {0, -1}};
        rows = board.size();
        cols = board[0].size();
        for (string word : words) {
            us.insert(word);
        }
        string path;
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                visited[r][c] = true;
                path += board[r][c];
                dfs(r, c, path);
                path = "";
                visited[r][c] = false;
            }
        }
        return ans;
    }

    void dfs(int row, int col, string& path) {
        if (path.length() > 10) return;
        if (us.count(path) == 1) {
            ans.push_back(path);
            us.erase(path);
        }
        for (pair<int, int> dir : direction) {
            int nr = row + dir.first;
            int nc = col + dir.second;
            if (0 <= nr && nr < rows && 0 <= nc && nc < cols) {
                if (!visited[nr][nc]) {
                    visited[nr][nc] = true;
                    path += board[nr][nc];
                    dfs(nr, nc, path);
                    path.erase(path.size() - 1);
                    visited[nr][nc] = false;
                }
            }
        }
    }
};
```

## 方法二：字典树+回溯

在「解法一」中，对于任意一个当前位置 (i, j)，我们都不可避免的搜索了四联通的全部方向，这导致了那些无效搜索路径最终只有长度达到 10 才会被剪枝。

要进一步优化我们的搜索过程，需要考虑如何在每一步的搜索中进行剪枝。

我们可以使用 TrieTrie 结构进行建树，对于任意一个当前位置 (i, j) 而言，只有在 Trie 中存在往从字符 a 到 b 的边时，我们才在棋盘上搜索从 a 到 b 的相邻路径。

与此同时，我们需要将平时建 TrieNode 中的 isEnd 标记属性直接换成记录当前字符 s，这样我们在 DFS 的过程中则无须额外记录当前搜索字符串。

执行用时：436 ms, 在所有 C++ 提交中击败了59.24%的用户

内存消耗：12.2 MB, 在所有 C++ 提交中击败了40.29%的用户

```c++
class Trie {
public:
    Trie* son[26];  // 存放当前字符之后的字符
    bool isWord;
    string str;
    Trie() {
        for (int i = 0; i < 26; i++) son[i] = nullptr;
        isWord = false;
        str = "";
    }
    void insert(string word) {
        Trie* root = this;     // 从头节点开始查
        for (char c : word) {  // 类似链表的遍历
            int cur = c - 'a';
            if (root->son[cur] == nullptr) root->son[cur] = new Trie();
            root = root->son[cur];
        }
        root->isWord = true;  // 在单词的结尾节点标记一下 是单词
        root->str = word;     // 结尾直接记录单词
    }
};

class Solution {
public:
    vector<vector<char>> board;
    Trie trie;
    int rows;
    int cols;
    vector<pair<int, int>> direction;
    bool visited[12][12];
    unordered_set<string> ans_set;
    vector<string> ans;

    vector<string> findWords(vector<vector<char>>& _board, vector<string>& words) {
        board = _board;
        rows = board.size();
        cols = board[0].size();
        direction = {{1, 0}, {0, 1}, {-1, 0}, {0, -1}};
        for (string word : words) {
            trie.insert(word);
        }

        for (int r = 0; r < rows; ++r) {
            for (int c = 0; c < cols; ++c) {
                int cur = board[r][c] - 'a';
                if (trie.son[cur]) {
                    visited[r][c] = true;
                    dfs(r, c, trie.son[cur]);
                    visited[r][c] = false;
                }
            }
        }
        for (string s : ans_set) ans.push_back(s);
        return ans;
    }
    void dfs(int row, int col, Trie* node) {
        if (node->str != "") {
            ans_set.insert(node->str);
        }
        for (pair<int, int> dir : direction) {
            int nr = row + dir.first;
            int nc = col + dir.second;
            if (0 <= nr && nr < rows && 0 <= nc && nc < cols) {
                if (!visited[nr][nc]) {
                    int nidx = board[nr][nc] - 'a';
                    if (node->son[nidx] != nullptr) {
                        visited[nr][nc] = true;
                        dfs(nr, nc, node->son[nidx]);
                        visited[nr][nc] = false;
                    }
                }
            }
        }
    }
};
```

function 写法，可见 dfs 写外面会快一些

执行用时：596 ms, 在所有 C++ 提交中击败了49.25%的用户

内存消耗：12.1 MB, 在所有 C++ 提交中击败了54.88%的用户

```c++
class Trie {
public:
    Trie* son[26];  // 存放当前字符之后的字符
    bool isWord;
    string str;
    Trie() {
        for (int i = 0; i < 26; i++) son[i] = nullptr;
        isWord = false;
        str = "";
    }
    void insert(string word) {
        Trie* root = this;     // 从头节点开始查
        for (char c : word) {  // 类似链表的遍历
            int cur = c - 'a';
            if (root->son[cur] == nullptr) root->son[cur] = new Trie();
            root = root->son[cur];
        }
        root->isWord = true;  // 在单词的结尾节点标记一下 是单词
        root->str = word;     // 结尾直接记录单词
    }
};

class Solution {
public:
    bool visited[12][12];

    vector<string> findWords(vector<vector<char>>& board, vector<string>& words) {
        Trie trie;
        vector<string> ans;
        unordered_set<string> ans_set;
        int rows = board.size();
        int cols = board[0].size();
        vector<pair<int, int>> direction = {{1, 0}, {0, 1}, {-1, 0}, {0, -1}};
        for (string word : words) {
            trie.insert(word);
        }

        function<void(int, int, Trie*)> dfs = [&](int row, int col, Trie* node) {
            if (node->str != "") {
                ans_set.insert(node->str);
            }
            for (pair<int, int> dir : direction) {
                int nr = row + dir.first;
                int nc = col + dir.second;
                if (0 <= nr && nr < rows && 0 <= nc && nc < cols) {
                    if (!visited[nr][nc]) {
                        int nidx = board[nr][nc] - 'a';
                        if (node->son[nidx] != nullptr) {
                            visited[nr][nc] = true;
                            dfs(nr, nc, node->son[nidx]);
                            visited[nr][nc] = false;
                        }
                    }
                }
            }
        };

        for (int r = 0; r < rows; ++r) {
            for (int c = 0; c < cols; ++c) {
                int cur = board[r][c] - 'a';
                if (trie.son[cur]) {
                    visited[r][c] = true;
                    dfs(r, c, trie.son[cur]);
                    visited[r][c] = false;
                }
            }
        }
        for (string s : ans_set) ans.push_back(s);
        return ans;
    }
};
```

