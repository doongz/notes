题目：[剑指 Offer II 033. 变位词组](https://leetcode.cn/problems/sfvd7V/)

给定一个字符串数组 `strs` ，将 **变位词** 组合在一起。 可以按任意顺序返回结果列表。

**注意：**若两个字符串中每个字符出现的次数都相同，则称它们互为变位词。

```
示例 1:

输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
输出: [["bat"],["nat","tan"],["ate","eat","tea"]]

示例 2:

输入: strs = [""]
输出: [[""]]

示例 3:

输入: strs = ["a"]
输出: [["a"]]
```

**提示：**

- `1 <= strs.length <= 104`
- `0 <= strs[i].length <= 100`
- `strs[i]` 仅包含小写字母

注意：本题与主站 49 题相同： https://leetcode-cn.com/problems/group-anagrams/

```python
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        hash_map = collections.defaultdict(list)
        for st in strs:
            cnter = [0 for _ in range(26)]
            for c in st:
                cnter[ord(c) - 97] += 1
            key = ",".join(map(str, cnter))
            hash_map[key].append(st)
            
        ans = []
        for key in hash_map:
            ans.append(hash_map[key])
        return ans
```

