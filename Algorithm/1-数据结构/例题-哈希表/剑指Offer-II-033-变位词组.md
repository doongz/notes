题目：[剑指 Offer II 033. 变位词组](https://leetcode.cn/problems/sfvd7V/)

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

