题目：[剑指 Offer II 034. 外星语言是否排序](https://leetcode.cn/problems/lwyVBB/)

某种外星语也使用英文小写字母，但可能顺序 `order` 不同。字母表的顺序（`order`）是一些小写字母的排列。

给定一组用外星语书写的单词 `words`，以及其字母表的顺序 `order`，只有当给定的单词在这种外星语中按字典序排列时，返回 `true`；否则，返回 `false`。

```
示例 1：

输入：words = ["hello","leetcode"], order = "hlabcdefgijkmnopqrstuvwxyz"
输出：true
解释：在该语言的字母表中，'h' 位于 'l' 之前，所以单词序列是按字典序排列的。

示例 2：

输入：words = ["word","world","row"], order = "worldabcefghijkmnpqstuvxyz"
输出：false
解释：在该语言的字母表中，'d' 位于 'l' 之后，那么 words[0] > words[1]，因此单词序列不是按字典序排列的。

示例 3：

输入：words = ["apple","app"], order = "abcdefghijklmnopqrstuvwxyz"
输出：false
解释：当前三个字符 "app" 匹配时，第二个字符串相对短一些，然后根据词典编纂规则 "apple" > "app"，因为 'l' > '∅'，其中 '∅' 是空白字符，定义为比任何其他字符都小（更多信息）。
```

提示：

1 <= words.length <= 100
1 <= words[i].length <= 20
order.length == 26
在 words[i] 和 order 中的所有字符都是英文小写字母。

注意：本题与主站 953 题相同： https://leetcode-cn.com/problems/verifying-an-alien-dictionary/

---

```cpp
class Solution {
public:
    vector<int> order_map;

    bool cmp(string &w1, string &w2) {
        // <= return true
        int n = min(w1.size(), w2.size());
        for (int i = 0; i < n; i++) {
            // cout << i << ": " << w1[i] << "," << w2[i] << endl;
            int idx1 = order_map[w1[i]-'a'];
            int idx2 = order_map[w2[i]-'a'];
            if (idx1 < idx2) {
                return true;
            } else if (idx1 > idx2) {
                return false;
            }
        }
        if (w1.size() == n && w2.size() == n) return true;
        if (w1.size() > n) return false;
        return true;
    }
    bool isAlienSorted(vector<string>& words, string order) {
        order_map.resize(26, 0);
        for (int i = 0; i < 26; i++) {
            order_map[order[i] - 'a'] = i;
        }
        int n = words.size();
        for (int i = 0; i < n - 1; i++) {
            if (!cmp(words[i], words[i+1])) {
                return false;
            }
            // cout << "**********" << endl;
        }
        return true;
    }
};
```

