from typing import Optional, List
from collections import deque

# Definition for a binary tree node.


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def create_tree_from_level_order(data: List[Optional[int]]) -> Optional[TreeNode]:
    """
    Create a binary tree from level-order array representation.
    None values in the array represent empty nodes.

    Args:
        data: List of integers or None values in level-order sequence

    Returns:
        Root node of the created tree, or None if input is empty
    """
    if not data or data[0] is None:
        return None

    root = TreeNode(data[0])  # Root node
    queue = deque([root])     # Queue for level-order insertion
    index = 1                 # Index in the data list

    while queue and index < len(data):
        node = queue.popleft()  # Get the current node

        # Assign the left child if available
        if index < len(data):
            if data[index] is not None:
                node.left = TreeNode(data[index])
                queue.append(node.left)
            index += 1

        # Assign the right child if available
        if index < len(data):
            if data[index] is not None:
                node.right = TreeNode(data[index])
                queue.append(node.right)
            index += 1

    return root


def print_tree_level_order(root: Optional[TreeNode]) -> None:
    """
    Print the level-order representation of a tree (breadth-first).

    Args:
        root: Root node of the binary tree
    """
    if not root:
        print("Empty tree")
        return

    queue = deque([root])
    result = []

    while queue:
        node = queue.popleft()
        if node:
            result.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        else:
            result.append("None")

    # Remove trailing None values
    while result and result[-1] == "None":
        result.pop()

    print("[" + ", ".join(result) + "]")


def inorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """
    Perform an inorder traversal of the binary tree.

    Args:
        root: Root node of the binary tree

    Returns:
        List of values in inorder sequence
    """
    result = []

    def traverse(node):
        if node:
            traverse(node.left)
            result.append(node.val)
            traverse(node.right)

    traverse(root)
    return result


def print_inorder_traversal(root: Optional[TreeNode]) -> None:
    """
    Print an inorder traversal of the binary tree.

    Args:
        root: Root node of the binary tree
    """
    values = inorder_traversal(root)
    print(" ".join(map(str, values)))


# Example usage
if __name__ == "__main__":
    # Level-order representations
    data1 = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
    data3 = [1, 2]

    # Create the trees
    tree1 = create_tree_from_level_order(data1)
    tree3 = create_tree_from_level_order(data3)

    # Print level-order representation
    print("Level-order representations:")
    print("Tree 1:", end=" ")
    print_tree_level_order(tree1)
    print("Tree 3:", end=" ")
    print_tree_level_order(tree3)

    # Print inorder traversals
    print("\nInorder traversals:")
    print("Tree 1:", end=" ")
    print_inorder_traversal(tree1)
    print("Tree 3:", end=" ")
    print_inorder_traversal(tree3)
