from typing import List


class Solution:

    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        print(nums1)
        nums1[m:m+n] = nums2
        print(nums1)
        nums1.sort()
        print(nums1)

    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        for i in s:
            print(i)
            print(f"$i $index(i+1)")
        return False

solution = Solution()

solution.wordBreak("leetcode", ["leet", "code"])

#solution.merge([1,2,3,0,0,0],3,[2,5,6],3)