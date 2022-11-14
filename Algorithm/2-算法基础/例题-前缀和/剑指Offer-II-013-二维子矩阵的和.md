题目：[剑指 Offer II 013. 二维子矩阵的和](https://leetcode.cn/problems/O4NDxx/)

给定一个二维矩阵 `matrix`，以下类型的多个请求：

- 计算其子矩形范围内元素的总和，该子矩阵的左上角为 `(row1, col1)` ，右下角为 `(row2, col2)` 。

实现 `NumMatrix` 类：

- `NumMatrix(int[][] matrix)` 给定整数矩阵 `matrix` 进行初始化
- `int sumRegion(int row1, int col1, int row2, int col2)` 返回左上角`(row1, col1)` 、右下角 `(row2, col2)` 的子矩阵的元素总和。

**示例 1：**

![img](https://pic.leetcode-cn.com/1626332422-wUpUHT-image.png)

```
输入: 
["NumMatrix","sumRegion","sumRegion","sumRegion"]
[[[[3,0,1,4,2],[5,6,3,2,1],[1,2,0,1,5],[4,1,0,1,7],[1,0,3,0,5]]],[2,1,4,3],[1,1,2,2],[1,2,2,4]]
输出: 
[null, 8, 11, 12]

解释:
NumMatrix numMatrix = new NumMatrix([[3,0,1,4,2],[5,6,3,2,1],[1,2,0,1,5],[4,1,0,1,7],[1,0,3,0,5]]]);
numMatrix.sumRegion(2, 1, 4, 3); // return 8 (红色矩形框的元素总和)
numMatrix.sumRegion(1, 1, 2, 2); // return 11 (绿色矩形框的元素总和)
numMatrix.sumRegion(1, 2, 2, 4); // return 12 (蓝色矩形框的元素总和)

```

提示：

m == matrix.length
n == matrix[i].length
1 <= m, n <= 200
`-105 <= matrix[i][j] <= 105`
0 <= row1 <= row2 < m
0 <= col1 <= col2 < n
最多调用 104 次 sumRegion 方法

注意：本题与主站 304 题相同： https://leetcode-cn.com/problems/range-sum-query-2d-immutable/



```c++
class NumMatrix {
public:
    vector<vector<int>> pre_sum;
    int rows;
    int cols;

    NumMatrix(vector<vector<int>>& matrix) {
        rows = matrix.size();
        cols = matrix[0].size();
        pre_sum.resize(rows + 1, vector<int>(cols + 1, 0));
        for (int r = 1; r < rows + 1; r++) {
            for (int c = 1; c < cols + 1; c++) {
                pre_sum[r][c] = pre_sum[r - 1][c] + pre_sum[r][c - 1] - pre_sum[r - 1][c - 1] + matrix[r - 1][c - 1];
            }
        }
    }

    int sumRegion(int row1, int col1, int row2, int col2) {
        return pre_sum[row2 + 1][col2 + 1] - pre_sum[row2 + 1][col1] - pre_sum[row1][col2 + 1] + pre_sum[row1][col1];
    }
};

/**
 * Your NumMatrix object will be instantiated and called as such:
 * NumMatrix* obj = new NumMatrix(matrix);
 * int param_1 = obj->sumRegion(row1,col1,row2,col2);
 */
```

