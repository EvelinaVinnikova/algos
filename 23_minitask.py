# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def balanceBST(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def inorder(node):
            if not node:
                return []
            return inorder(node.left) + [node.val] + inorder(node.right)
        
        def build_balanced_bst(nums):
            if not nums:
                return None
            mid = len(nums) // 2
            node = TreeNode(nums[mid])
            node.left = build_balanced_bst(nums[:mid])
            node.right = build_balanced_bst(nums[mid+1:])
            return node
        
        sorted_vals = inorder(root)
        return build_balanced_bst(sorted_vals)
