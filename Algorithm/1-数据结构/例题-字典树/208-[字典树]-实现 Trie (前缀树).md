[208. 实现 Trie (前缀树)](https://leetcode-cn.com/problems/implement-trie-prefix-tree/)

## c++

```c++
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

