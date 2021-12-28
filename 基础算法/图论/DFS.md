# DFS 深度优先搜索

Depth First Search

## 遍历



## 回溯

```python
result = []
def backtrack(路径, 选择列表):
    if 满足结束条件:
        result.add(路径)
        return

    for 选择 in 选择列表:
        做选择
        backtrack(路径, 选择列表)
        撤销选择
```

## 记忆化 dfs



