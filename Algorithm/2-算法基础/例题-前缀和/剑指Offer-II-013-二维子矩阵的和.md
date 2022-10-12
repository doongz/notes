题目：[剑指 Offer II 013. 二维子矩阵的和](https://leetcode.cn/problems/O4NDxx/)

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

