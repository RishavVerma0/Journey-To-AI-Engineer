# 111. Minimum Depth of Binary Tree
# Solved
# Easy
# Topics
# premium lock icon
# Companies
# Given a binary tree, find its minimum depth.

# The minimum depth is the number of nodes along the shortest path from xml.dom.minidom import Node

# from the root node down to the nearest leaf node.

# Note: A leaf is a node with no children.

 

# Example 1:


# Input: root = [3,9,20,null,null,15,7]
# Output: 2
# Example 2:

# Input: root = [2,null,3,null,4,null,5,null,6]
# Output: 5
 

# Constraints:

# The number of nodes in the tree is in the range [0, 105].
# -1000 <= Node.val <= 1000

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from collections import deque
class Solution:
    def minDepth(self, root: TreeNode) -> int: # type: ignore
        if not root:
            return 0  # If the tree is empty, return depth 0
        
        queue = deque([(root, 1)])  # Initialize the queue with the root node and depth 1
        
        while queue:
            node, depth = queue.popleft()
            
            # If it's a leaf node, return the current depth
            if not node.left and not node.right:
                return depth
            
            # Add left and right children to the queue, if they exist
            if node.left:
                queue.append((node.left, depth + 1))
            if node.right:
                queue.append((node.right, depth + 1))