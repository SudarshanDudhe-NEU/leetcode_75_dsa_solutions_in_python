import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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

    root = TreeNode(data[0])
    queue = deque([root])
    index = 1

    while queue and index < len(data):
        node = queue.popleft()

        if index < len(data) and data[index] is not None:
            node.left = TreeNode(data[index])
            queue.append(node.left)
        index += 1

        if index < len(data) and data[index] is not None:
            node.right = TreeNode(data[index])
            queue.append(node.right)
        index += 1

    return root


class Solution:
    def __init__(self):
        self.max_zigzag_path_length = 0
        self.zigzag_path = []
        self.tree_edges = []
        self.zigzag_edges = []

    def longest_zigzag(self, root: TreeNode) -> int:
        def dfs(node, direction, path_length, path_nodes):
            if not node:
                return

            if path_length > self.max_zigzag_path_length:
                self.max_zigzag_path_length = path_length
                self.zigzag_path = path_nodes.copy()

            dfs(node.left, "left", 1 if direction == "left" else path_length +
                1, path_nodes + [node.left]) if node.left else None
            dfs(node.right, "right", 1 if direction == "right" else path_length +
                1, path_nodes + [node.right]) if node.right else None

        if root.left:
            dfs(root.left, "left", 1, [root.left])
        if root.right:
            dfs(root.right, "right", 1, [root.right])

        self.visualize_tree_animation(root)
        return self.max_zigzag_path_length

    def visualize_tree_animation(self, root):
        G = nx.DiGraph()
        pos = {}

        def traverse(node, x=0, y=0, level=1):
            if node:
                G.add_node(node.val)
                pos[node.val] = (x, -y)
                if node.left:
                    self.tree_edges.append((node.val, node.left.val))
                    traverse(node.left, x - 2 / level, y + 1, level * 1.5)
                if node.right:
                    self.tree_edges.append((node.val, node.right.val))
                    traverse(node.right, x + 2 / level, y + 1, level * 1.5)

        traverse(root)

        # Identify the zigzag edges separately
        self.zigzag_edges = [(self.zigzag_path[i].val, self.zigzag_path[i + 1].val)
                             for i in range(len(self.zigzag_path) - 1)]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_title("Binary Tree Visualization (Animated)")

        def update(frame):
            ax.clear()
            ax.set_title("Binary Tree Visualization (Animated)")

            nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue",
                    font_size=12, edge_color="gray", ax=ax)

            if frame < len(self.tree_edges):
                nx.draw_networkx_edges(G, pos, edgelist=self.tree_edges[:frame + 1],
                                       edge_color="black", width=2, ax=ax)

            if frame >= len(self.tree_edges):
                nx.draw_networkx_edges(
                    G, pos, edgelist=self.zigzag_edges, edge_color="red", width=3, ax=ax)

        ani = animation.FuncAnimation(fig, update, frames=len(
            self.tree_edges) + 10, interval=500, repeat=False)
        plt.show()


# Level-order representation of a tree
data1 = [1, None, 1, 1, 1, None, None, 1, 1, None, 1, None, None, None, 1]

# Create tree
tree1 = create_tree_from_level_order(data1)

# Run the Solution
sol = Solution()
print("Longest Zigzag Path Length in Tree 1:", sol.longest_zigzag(tree1))

# # Level-order representations of trees
# data1 = [1, None, 1, 1, 1, None, None, 1, 1, None, 1, None, None, None, 1]
# data2 = [1, 1, 1, None, 1, None, None, 1, 1, None, 1]
# data3 = [1]

# # Create the trees
# tree1 = create_tree_from_level_order(data1)
# # tree2 = create_tree_from_level_order(data2)
# # tree3 = create_tree_from_level_order(data3)

# # Print inorder traversal of the trees
# print("Tree 1 (Inorder Traversal):")
# inorder_traversal(tree1)
# # print("\nTree 2 (Inorder Traversal):")
# # inorder_traversal(tree2)
# # print("\nTree 3 (Inorder Traversal):")
# # inorder_traversal(tree3)

# # Run the Solution's longest_zigzag function on the trees
# sol = Solution()

# print("\nLongest Zigzag Path Length in Tree 1:", sol.longest_zigzag(tree1))
# # print("Longest Zigzag Path Length in Tree 2:", sol.longest_zigzag(tree2))
# # print("Longest Zigzag Path Length in Tree 3:", sol.longest_zigzag(tree3))
