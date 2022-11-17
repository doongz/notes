题目：[133. 克隆图](https://leetcode-cn.com/problems/clone-graph/)

给你无向 **[连通](https://baike.baidu.com/item/连通图/6460995?fr=aladdin)** 图中一个节点的引用，请你返回该图的 [**深拷贝**](https://baike.baidu.com/item/深拷贝/22785317?fr=aladdin)（克隆）。

图中的每个节点都包含它的值 `val`（`int`） 和其邻居的列表（`list[Node]`）。

```
class Node {
    public int val;
    public List<Node> neighbors;
}
```

```
输入：adjList = [[2,4],[1,3],[2,4],[1,3]]
输出：[[2,4],[1,3],[2,4],[1,3]]
解释：
图中有 4 个节点。
节点 1 的值是 1，它有两个邻居：节点 2 和 4 。
节点 2 的值是 2，它有两个邻居：节点 1 和 3 。
节点 3 的值是 3，它有两个邻居：节点 2 和 4 。
节点 4 的值是 4，它有两个邻居：节点 1 和 3 。

输入：adjList = [[]]
输出：[[]]
解释：输入包含一个空列表。该图仅仅只有一个值为 1 的节点，它没有任何邻居。

输入：adjList = []
输出：[]
解释：这个图是空的，它不含任何节点。

输入：adjList = [[2],[1]]
输出：[[2],[1]]

```

提示：

节点数不超过 100 。
每个节点值 Node.val 都是唯一的，1 <= Node.val <= 100。
无向图是一个简单图，这意味着图中没有重复的边，也没有自环。
由于图是无向的，如果节点 p 是节点 q 的邻居，那么节点 q 也必须是节点 p 的邻居。
图是连通图，你可以从给定节点访问到所有节点。

## 方法一：dfs

```c++
class Solution {
public:
    unordered_map<int, Node*> visited;

    Node* dfs(Node* node) {
        if (node == nullptr) return nullptr;
        if (visited.count(node->val)) return visited[node->val];

        Node* copyNode = new Node(node->val);
        visited[node->val] = copyNode;
        for (Node* nextNode : node->neighbors) {
            copyNode->neighbors.push_back(dfs(nextNode));
        }
        return copyNode;
    }

    Node* cloneGraph(Node* node) {
        return dfs(node);
        ;
    }
};
```

执行用时：40 ms, 在所有 Python3 提交中击败了56.04%的用户

内存消耗：15.4 MB, 在所有 Python3 提交中击败了31.73%的用户

```python
"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        
        def dfs(node):
            if not node: return None
            if node in visited: return visited[node]            

            clone = Node(node.val)
            visited[node] = clone
            for n_node in node.neighbors:
                clone.neighbors.append(dfs(n_node))

            return clone
        
        visited = {}
        return dfs(node)
```

执行用时：0 ms, 在所有 Go 提交中击败了100.00%的用户

内存消耗：2.9 MB, 在所有 Go 提交中击败了76.75%的用户

```go
/**
 * Definition for a Node.
 * type Node struct {
 *     Val int
 *     Neighbors []*Node
 * }
 */

func cloneGraph(node *Node) *Node {
	visited := map[*Node]*Node{}

	var dfs func(node *Node) *Node
	dfs = func(node *Node) *Node {
		if node == nil {
			return nil
		}
		if _, ok := visited[node]; ok {
			return visited[node]
		}
		clone := &Node{node.Val, []*Node{}}
		visited[node] = clone
		for _, n_node := range node.Neighbors {
			visited[node].Neighbors = append(visited[node].Neighbors, dfs(n_node))
		}
		return clone
	}

	return dfs(node)
}
```

## 方法二：bfs

**重建图和遍历图不一样的地方**：

**需要用 visited 保存 原图中的节点 和 克隆图中对应的节点**

```c++
class Solution {
public:
    Node* cloneGraph(Node* node) {
        if (node == nullptr) return nullptr;

        queue<Node*> que;
        que.push(node);
        Node* copyRoot = new Node(node->val);
        // key:原图中的节点 val:克隆图中对应的节点
        unordered_map<Node*, Node*> visited = {{node, copyRoot}};

        while (!que.empty()) {
            Node* cur = que.front();
            que.pop();
            for (Node* nextNode : cur->neighbors) {
                if (visited.count(nextNode) == 0) {
                    que.push(nextNode);
                    visited[nextNode] = new Node(nextNode->val);
                }
                visited[cur]->neighbors.push_back(visited[nextNode]);
            }
        }
        return copyRoot;
    }
};

```

执行用时：40 ms, 在所有 Python3 提交中击败了56.04%的用户

内存消耗：15.4 MB, 在所有 Python3 提交中击败了46.98%的用户

```python
"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""

class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        if not node: return None
        clone = Node(node.val)
        queue = [node]
        visited = {node: clone} # key:原图中的节点 val:克隆图中对应的节点

        while queue:
            node = queue.pop(0)
            for n_node in node.neighbors:
                if n_node not in visited:
                    queue.append(n_node)
                    visited[n_node] = Node(n_node.val) # 只有没来过的点需要初始化下
                # 将当前节点在克隆图中对应的节点 的 相邻点 添加上
                visited[node].neighbors.append(visited[n_node])
        return clone
```

执行用时：0 ms, 在所有 Go 提交中击败了100.00%的用户

内存消耗：2.9 MB, 在所有 Go 提交中击败了35.06%的用户

```go
/**
 * Definition for a Node.
 * type Node struct {
 *     Val int
 *     Neighbors []*Node
 * }
 */

func cloneGraph(node *Node) *Node {
	if node == nil {
		return nil
	}
	clone := Node{node.Val, []*Node{}}
	queue := []*Node{node}
	visited := map[*Node]*Node{}
	visited[node] = &clone

	for len(queue) > 0 {
		node := queue[0]
		queue = queue[1:]
		for _, n_node := range node.Neighbors {
			if _, ok := visited[n_node]; !ok {
				queue = append(queue, n_node)
				visited[n_node] = &Node{n_node.Val, []*Node{}}
			}
			visited[node].Neighbors = append(visited[node].Neighbors, visited[n_node])
		}
	}

	return &clone
}
```

