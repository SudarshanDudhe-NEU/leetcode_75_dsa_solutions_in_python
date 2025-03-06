from typing import Optional, List
from collections import deque

# Definition for a binary tree node.


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def create_tree_from_level_order(data: List[Optional[int]]) -> Optional[TreeNode]:
    if not data or data[0] is None:
        return None

    root = TreeNode(data[0])  # Root node
    queue = deque([root])      # Queue for level-order insertion
    index = 1                  # Index in the data list

    while queue and index < len(data):
        node = queue.popleft()  # Get the current node

        # Assign the left child if available
        if index < len(data) and data[index] is not None:
            node.left = TreeNode(data[index])
            queue.append(node.left)
        index += 1

        # Assign the right child if available
        if index < len(data) and data[index] is not None:
            node.right = TreeNode(data[index])
            queue.append(node.right)
        index += 1

    return root


def inorder_traversal(root: Optional[TreeNode]):
    """Performs inorder traversal of the binary tree and prints the node values."""
    if root:
        inorder_traversal(root.left)
        print(root.val, end=" ")
        inorder_traversal(root.right)


# Level-order representations of trees
data1 = [1, None, 1, 1, 1, None, None, 1, 1, None, 1, None, None, None, 1]
data2 = [1, 1, 1, None, 1, None, None, 1, 1, None, 1]
data3 = [1]

# Create the trees
tree1 = create_tree_from_level_order(data1)
tree2 = create_tree_from_level_order(data2)

# Print inorder traversal of the trees
print("Tree 1 (Inorder Traversal):")
inorder_traversal(tree1)
print("\nTree 2 (Inorder Traversal):")
inorder_traversal(tree2)


class Solution:
    def __init__(self):
        self.max_zig_zag_path_length = 0

    def longestZigZag(self, root):
        def calculate_zigzag_path_length(node, direction, path_length):
            if not node:
                return

            self.max_zig_zag_path_length = max(
                self.max_zig_zag_path_length, path_length)

            if direction == "right":
                calculate_zigzag_path_length(node.left, "left", path_length+1)
                calculate_zigzag_path_length(node.right, "right", 1)
            else:
                calculate_zigzag_path_length(
                    node.right, "right", path_length+1)
                calculate_zigzag_path_length(node.left, "left", 1)

        if not root:
            return 0
        calculate_zigzag_path_length(root.left, "left", 1)
        calculate_zigzag_path_length(root.right, "right", 1)

        return self.max_zig_zag_path_length
