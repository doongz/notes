遍历：

while queue 非空:

        node = queue.pop()

    for node 的所有相邻结点 m:

        if m 未访问过:

            queue.push(m)

求最短路径：

depth = 0 # 记录遍历到第几层

while queue 非空:

    depth++

    n = queue 中的元素个数

    循环 n 次:

        node = queue.pop()

        for node 的所有相邻结点 m:

            if m 未访问过:

                queue.push(m)

                 

