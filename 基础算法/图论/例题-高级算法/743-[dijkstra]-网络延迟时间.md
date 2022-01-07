#### [743. 网络延迟时间](https://leetcode-cn.com/problems/network-delay-time/)

**方法一：dijkstra**

时间复杂度：`O(n*logn)`，假设每个点都与其余的点相连

空间复杂度：`O(n^2)`

执行用时：72 ms, 在所有 Python3 提交中击败了64.95%的用户

内存消耗：16.2 MB, 在所有 Python3 提交中击败了52.87%的用户

```python
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # 邻接表 u -> v w
        adj = collections.defaultdict(list)
        for u, v, w in times:
            adj[u].append((v, w))
        dis = [float("inf") for _ in range(n+1)] # 记录结点最早收到信号的时间
        dis[k] = 0
        print(adj)

        queue = []
        heapq.heappush(queue, (dis[k], k)) # 小根堆
        visited = set() # 记录已经找到的最小值了的点
        while queue:
            _, cur = heappop(queue)
            if cur in visited:
                # 优先队列pop出的为最小值，已经确定的值，下次不用再走了
                continue
            visited.add(cur)
            for n_node, cost in adj[cur]:
                tmp = dis[cur] + cost
                if tmp < dis[n_node]:
                    dis[n_node] = tmp
                    heapq.heappush(queue, (dis[n_node], n_node))
        # print(dis)
        ans = 0
        for t in dis[1:]:
            if t == float("inf"):
                return -1
            ans = max(ans, t)
        return ans
```



**方法二：bfs**

时间复杂度：`O(n^2)`，假设每个点都与其余的点相连

空间复杂度：`O(n^2)`

执行用时：92 ms, 在所有 Python3 提交中击败了34.12%的用户

内存消耗：16.3 MB, 在所有 Python3 提交中击败了25.25%的用户

```python
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # 邻接表 u -> v w
        adj = collections.defaultdict(list)
        for u, v, w in times:
            adj[u].append((v, w))
        
        queue = [(k, 0)]
        dis = [-1 for _ in range(n+1)] # 记录结点最早收到信号的时间
        dis[k] = 0
        while queue:
            cur, path = queue.pop(0)
            for n_node, cost in adj[cur]:
                if dis[n_node] == -1 or path + cost < dis[n_node]:
                    # 仅当结点未收到或收到时间比记录时间更早才更新并入队
                    dis[n_node] = path + cost
                    queue.append((n_node, path + cost))
        ans = 0
        for t in dis[1:]:
            if t == -1:
                return -1
            ans = max(ans, t)
        return ans
```

**方法三：dfs + 剪枝**

时间复杂度：`O(n^n)`，假设每个点都与其余的点相连

空间复杂度：`O(n)`，邻接表 `O(n)`，递归栈`O(n)`

执行用时：3484 ms, 在所有 Python3 提交中击败了5.07%的用户

内存消耗：17.4 MB, 在所有 Python3 提交中击败了5.32%的用户

```python
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # 邻接表 u -> v w
        adj = collections.defaultdict(list)
        for u, v, w in times:
            adj[u].append((v, w))
        dis = [-1 for _ in range(n+1)]
        dis[k] = 0
        
        def dfs(node, path):
            for n_node, cost in adj[node]:
                if dis[n_node] == -1 or path + cost < dis[n_node]:
                    # 如果没有到达，且路径比以前短，才能进入递归
                    dis[n_node] = path + cost
                    dfs(n_node, path + cost)
        
        dfs(k, 0)
        ans = 0
        for t in dis[1:]:
            if t == -1:
                return -1
            ans = max(ans, t)
        return ans
```



`感谢`  大家点赞 Star🌟 [https://github.com/DoWalle/algorithm](https://github.com/DoWalle/algorithm) 笔芯🤞

`发布`  于 Gitbook [https://dowalle.gitbook.io/algo/](https://dowalle.gitbook.io/algo/)

