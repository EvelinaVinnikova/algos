from collections import deque

# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None


class Codec:

    def serialize(self, root) -> str:
        """Encodes a tree to a single string.
        :type root: TreeNode
        :rtype: str
        """
        if not root or root.val == 'null':
            return 'null,'
        return f"{root.val}," + self.serialize(root.left) + self.serialize(root.right)


    def deserialize(self, data) -> TreeNode:
        """
        Decodes your encoded data to tree.
        :type data: str
        :rtype: TreeNode
        """
        if not data:
            return None

        nodes = deque(data.split(','))
        
        def build():
            if not nodes:
                return None
            val = nodes.popleft()
            if val == 'null' or val == '':
                return None
            node = TreeNode(int(val))
            node.left = build()
            node.right = build()
            return node

        return build()

        

# Your Codec object will be instantiated and called as such:
# ser = Codec()
# deser = Codec()
# ans = deser.deserialize(ser.serialize(root))
