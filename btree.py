import sys

sys.path.append('..')
from btnode import BTNode


class BTree:
    """
    Class for binary tree
    """

    def __init__(self):
        self.root = BTNode(1)

    def set_left(self, node):
        self.root.left = node

    def set_right(self, node):
        self.root.right = node
