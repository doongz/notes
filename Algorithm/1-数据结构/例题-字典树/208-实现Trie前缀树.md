[208. 实现 Trie (前缀树)](https://leetcode-cn.com/problems/implement-trie-prefix-tree/)

Trie（发音类似 "try"）或者说 前缀树 是一种树形数据结构，用于高效地存储和检索字符串数据集中的键。这一数据结构有相当多的应用情景，例如自动补完和拼写检查。

请你实现 Trie 类：

- Trie() 初始化前缀树对象。
- void insert(String word) 向前缀树中插入字符串 word 。
- boolean search(String word) 如果字符串 word 在前缀树中，返回 true（即，在检索之前已经插入）；否则，返回 false 。
- boolean startsWith(String prefix) 如果之前已经插入的字符串 word 的前缀之一为 prefix ，返回 true ；否则，返回 false 。

**示例：**

```
输入
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
输出
[null, null, true, false, true, null, true]

解释
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple");   // 返回 True
trie.search("app");     // 返回 False
trie.startsWith("app"); // 返回 True
trie.insert("app");
trie.search("app");     // 返回 True
```

提示：

1 <= word.length, prefix.length <= 2000
word 和 prefix 仅由小写英文字母组成
insert、search 和 startsWith 调用次数 总计 不超过 3 * 104 次

## c++

```cpp
class Trie {
private:
    Trie* son[26];  // 存放当前字符之后的字符
    bool isWord;

public:
    Trie() {
        for (int i = 0; i < 26; i++) son[i] = nullptr;
        isWord = false;
    }
    ~Trie() {
        for (int i = 0; i < 26; i++) {
            if (son[i] != nullptr) delete son[i];
        }
    }

    void insert(string word) {
        Trie* root = this;     // 从头节点开始查
        for (char c : word) {  // 类似链表的遍历
            int cur = c - 'a';
            if (root->son[cur] == nullptr) root->son[cur] = new Trie();
            root = root->son[cur];
        }
        root->isWord = true;  // 在单词的结尾节点标记一下 是单词
    }

    bool search(string word) {
        Trie* root = this;  // 从头节点开始查
        for (char c : word) {
            int cur = c - 'a';
            if (root->son[cur] == nullptr) return false;  // word还没遍历完，就找不到了
            root = root->son[cur];
        }
        return root->isWord;  // 遍历到word结尾的节点，是否是之前存在的单词
    }

    bool startsWith(string prefix) {
        Trie* root = this;
        for (char c : prefix) {
            int cur = c - 'a';
            if (root->son[cur] == nullptr) return false;  // prefix还没遍历完，就找不到了
            root = root->son[cur];
        }
        return true;  // prefix正常遍历完，就返回true
    }
};
```

## python

```python
class TrieNode(object):
    def __init__(self):
        self.children = {}
        self.is_word = False

class Trie(object):
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = TrieNode()

    def insert(self, word):
        """
        Inserts a word into the trie.
        :type word: str
        :rtype: None
        """
        node = self.root    # 从头节点开始查
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_word = True # 在单词的结尾节点标记一下

    def search_prefix(self, word):
        node = self.root    # 从头节点开始查
        for c in word:
            if c not in node.children:
                return None # word中的字符没找完就断了
            node = node.children[c]
        # 返回word结尾的节点，
        # 可能是之前插入单词的结尾节点，node.is_word 为 True
        # 不是之前插入单词的结尾节点，node.is_word 为 False
        return node         

    def search(self, word):
        """
        Returns if the word is in the trie.
        :type word: str
        :rtype: bool
        """
        node = self.search_prefix(word)
        return node != None and node.is_word

    def startsWith(self, prefix):
        """
        Returns if there is any word in the trie that starts with the given prefix.
        :type prefix: str
        :rtype: bool
        """
        return self.search_prefix(prefix) != None
```

