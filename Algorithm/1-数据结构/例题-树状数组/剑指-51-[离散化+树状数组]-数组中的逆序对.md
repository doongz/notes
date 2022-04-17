[剑指 Offer 51. 数组中的逆序对](https://leetcode-cn.com/problems/shu-zu-zhong-de-ni-xu-dui-lcof/)

与 [315. 计算右侧小于当前元素的个数](https://leetcode-cn.com/problems/count-of-smaller-numbers-after-self/solution/shu-zhuang-shu-zu-c-python-by-dodo_1202-igmr/) 一摸一样

```c++
class FenwickTree {
public:
    int size;
    vector<int> tree;

    FenwickTree(int n) {
        size = n;
        tree.resize(size + 1, 0);
    }
    int lowbit(int idx) {
        return idx & (-idx);
    }
    void add(int idx, int delta) {
        while (idx < size + 1) {
            tree[idx] += delta;
            idx += lowbit(idx);
        }
    }
    int query(int idx) {
        int sum = 0;
        while (idx > 0) {
            sum += tree[idx];
            idx -= lowbit(idx);
        }
        return sum;
    }
};

class Solution {
public:
    int reversePairs(vector<int>& nums) {
        set<int> s(nums.begin(), nums.end());
        unordered_map<int, int> um;
        int rank = 1;
        for (auto it = s.begin(); it != s.end(); it++) {
            um[*it] = rank;
            rank++;
        }
        FenwickTree ftree(s.size());
        int ans = 0;
        for (int i = nums.size() - 1; i >= 0; i--) {
            rank = um[nums[i]];
            ftree.add(rank, 1);
            ans += ftree.query(rank - 1);
        }
        return ans;
    }
};
```

