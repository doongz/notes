## 遍历

```python
queue = [node]
visited = set([node])
while queue 非空:
    node = queue.pop(0)
    for node 的所有相邻结点 next_node:
        if mnext_node not in visited: # 未访问过，不走回头路
            queue.append(next_node)
            visited.add(next_node)
```
## 求最短路径

节点深度可以和节点值一起记录

```python
queue = [(node, 0)] # (节点值, 节点深度)
visited = set([node])
while queue 非空:
    node, depth = queue.pop(0)
    if node 达到终点:
      return depth
    for node 的所有相邻结点 next_node:
        if m not in visited: # 未访问过，不走回头路
            queue.append((next_node, depth+1))
            visited.add(next_node)
```

其他语言不方便把不同类型的变量放到一个数组里是，可以将depth写到外面

```python
queue = [node]
visited = set([node])
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

## 双向bfs

```python
l_queue = [begin]
r_queue = [end]
l_visited = set([begin])
r_visited = set([end])
depth = 1

while l_queue and r_queue:

    if len(l_queue) > len(r_queue):
        # 每次都走短的一侧，能走最小的面积
        l_queue, r_queue = r_queue, l_queue
        l_visited, r_visited = r_visited, l_visited

    queue_sz = len(l_queue)
    for _ in range(queue_sz):   # 每层开始遍历
        cur = l_queue.pop(0)
        if cur in r_visited:    # 如果当前节点在另一侧走过，说明在这一层出现交点了
            return depth        # 找到相交时，两边合计做过的层数
        for cur 的所有相邻结点 next_node:
            if next_node not in l_visited:
                l_queue.append(n_node)
                l_visited.add(n_node)
    depth += 1
```

