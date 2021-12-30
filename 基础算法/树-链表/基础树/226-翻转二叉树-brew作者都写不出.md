bfs：

```python
class Solution:
    def invertTree(self, root: TreeNode) -> TreeNode:

        if not root:
            return None
        
        queue = collections.deque()
        queue.append(root)
        while queue:
            cur = queue.popleft()
            cur.left, cur.right = cur.right, cur.left
            
            if cur.left:
                queue.append(cur.left)
            if cur.right:
                queue.append(cur.right)
        return root
```

dfs:

```python
class Solution:
    def invertTree(self, root: TreeNode) -> TreeNode:

        if not root:
            return None
        # 先序遍历 自顶向下
        def dfs(node):
            if not node:
                return None
            rightTree = node.right
            node.right = dfs(node.left)
            node.left = dfs(rightTree)
            return node

        return dfs(root)
```

