遍历：

```python
queue = [node]
visited = set()
while queue 非空:
    node = queue.pop(0)
    for node 的所有相邻结点 m:
        if m 未访问过:
            queue.append(m)
            visited.add(m)
```
求最短路径：

```python
queue = [node]
visited = set()
depth = 0 # 记录遍历到第几层
while queue 非空:
    n = queue 中的元素个数
    循环 n 次:
        node = queue.pop()
        if node 为 目标值:
            return depth
        for node 的所有相邻结点 m:
            if m 未访问过:
                queue.append(m)
                visited.add(m)
    depth++
```