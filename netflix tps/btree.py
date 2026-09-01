class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

#  example binary tree:
#            1
#           / \ 
#         2    3
#        /      \
#      4         5


a = Node(1)
b = Node(2)
a.left = b
c = Node(3)
a.right = c

d = Node(4)
b.left = d
e = Node(5)
c.right = e


def dfs(node):
    if node is None:
        return
    print(node.data, end=" ")
    dfs(node.left)
    dfs(node.right)



dfs(a)  # Output: 1 2 4 3
print()  # for newline


def dfs_iterative(node):
    stack = [node]
    while stack:
        cur = stack.pop()
        if cur.left is not None:
            stack.append(cur.left)
            # print("stack", [n.data for n in stack])
        if cur.right is not None:
            stack.append(cur.right)
            # print("stack", [n.data for n in stack])
        print(cur.data, end=" ")
    print()  # for newline


dfs_iterative(a)  # Output: 1 3 2 4


from collections import deque

def bfs(node): # popleft ***************
    q = deque([node]) # only change this line to use deque instead of list
    while q:
        cur = q.popleft() # only change this line to use popleft() instead of pop(0)
        if cur.left is not None:
            q.append(cur.left)
        if cur.right is not None:
            q.append(cur.right)
        print(cur.data, end=" ")

bfs(a)  # Output: 1 2 3 4 5

print()  # for newline

def print_left_view(node):
    if node is None:
        return

    last_level = -1
    q = deque([(node, 0)])
    while q:
        cur, level = q.popleft()
        if level > last_level:
            print(cur.data, end=" ")
            last_level = level
        if cur.left is not None:
            q.append((cur.left, level + 1))
        if cur.right is not None:
            q.append((cur.right, level + 1))
        
print_left_view(a)  # Output: 1 2 4


print()  # for newline


def height(node):
    if node is None:
        return 0
    
    return 1 + max(height(node.left), height(node.right))

height_of_tree = height(a)
print("Height of the tree:", height_of_tree)  # Output: Height of the tree




# Given a binary tree, determine if it is height-balanced.
class Solution(object):
    def height(self, root):
        if root == None:
            return 0
        l = self.height(root.left)
        r = self.height(root.right)
        if l<0 or r<0 or abs (l-r) >1:
            return -1
        return 1 + max(l, r)
    
    def isBalanced(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: bool
        """
        return self.height(root) >= 0