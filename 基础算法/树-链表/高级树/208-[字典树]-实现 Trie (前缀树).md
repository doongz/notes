#### [208. 实现 Trie (前缀树)](https://leetcode-cn.com/problems/implement-trie-prefix-tree/)

```python
# python实现
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


class TrieNode(object):
    def __init__(self):
        self.children = {}
        self.is_word = False
```

