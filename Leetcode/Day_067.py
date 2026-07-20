# 49. Group Anagrams
# Solved
# Medium
# Topics
# premium lock icon
# Companies
# Given an array of strings strs, group the anagrams together. You can return the answer in any order.

 

# Example 1:

# Input: strs = ["eat","tea","tan","ate","nat","bat"]

# Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

# Explanation:

# There is no string in strs that can be rearranged to form "bat".
# The strings "nat" and "tan" are anagrams as they can be rearranged to form each other.
# The strings "ate", "eat", and "tea" are anagrams as they can be rearranged to form each other.
# Example 2:

# Input: strs = [""]

# Output: [[""]]

# Example 3:

# Input: strs = ["a"]

# Output: [["a"]]


from collections import defaultdict
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]: # type: ignore

        solution = defaultdict(list)

        for words in strs:
            key = "".join(sorted(words))
            solution[key].append(words)

        return list(solution.values())
    
def main():

    strs = ["ihlsa","hilsa","sahil","vrisha","ravish","rishav"]

    sol = Solution()

    result = sol.groupAnagrams(strs)

    print("Input:")

    print(strs)

    print("\nGrouped Anagrams:")

    for group in result:

        print(group)

if __name__ == "__main__":

    main()