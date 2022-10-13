

```c++
class Solution {
public:
    string str;
    int n;

    int mid(int i) {
        int res = 0;
        int l = i;
        int r = i;
        while (l >= 0 && r < n) {
            if (str[l] == str[r]) {
                res++;
            } else {
                break;
            }
            l--;
            r++;
        }
        return res;
    }

    int gap(int i) {  // i下标后的间隙
        int res = 0;
        int l = i;
        int r = i + 1;
        while (l >= 0 && r < n) {
            if (str[l] == str[r]) {
                res++;
            } else {
                break;
            }
            l--;
            r++;
        }
        return res;
    }

    int countSubstrings(string s) {
        str = s;
        n = s.size();
        int ans = 0;
        for (int i = 0; i < n; i++) {
            ans += mid(i);  // 从中心点扩散
        }
        for (int i = 0; i < n - 1; i++) {
            ans += gap(i);  // 从间隙扩散
        }
        return ans;
    }
};
```

