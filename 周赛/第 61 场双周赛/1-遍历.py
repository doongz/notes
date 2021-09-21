import collections

class Solution:
    def run(self, nums, k):
        size = len(nums)
        ans = 0
        if size == 1:
            return ans
        for i in range(size-1):
            for j in range(i+1, size):
                if abs(nums[i]-nums[j])==k:
                    ans += 1
        return ans


if __name__ == "__main__":
    nums = [1,2,2,1]
    k = 1
    res = Solution().run(nums, k)
    print(res)
