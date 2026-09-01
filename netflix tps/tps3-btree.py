# Given a starting movie and a number K, find all movies that are within K connections of the
# starting movie.

# For example:

#        B ─── D
#       /
# A ───
#       \
#        C ─── E ─── F


# Starting from A with K = 2:

# Distance 0: A
# Distance 1: B, C
# Distance 2: D, E

class Node:
    def __init__(self, data):
        self.data = data
        self.neighbors = [] # # not a binary tree, so we need to keep track of neighbors

from collections import deque

def BFS(start, k):
    visited = set() # not a binary tree, so we need to keep track of visited nodes
    q = deque([(start, 0)])

    while q:
        movie, distance = q.popleft()
        if movie in visited:
            continue
        visited.add(movie)
        if distance <= k:
            print(movie.data)
            for neighbor in movie.neighbors:
                q.append((neighbor, distance + 1))

# improvement: mark visited when you enqueue 
# Right now you mark a node visited when you pop it:


a = Node("A")
b = Node("B")
c = Node("C")
d = Node("D")
e = Node("E")
f = Node("F")

a.neighbors = [b, c]
b.neighbors = [a, d]
c.neighbors = [a, e]
d.neighbors = [b]
e.neighbors = [c, f]
f.neighbors = [e]


BFS(a, 2)




# Given a graph of movies and a starting movie and target movie, return the shortest path between them.

# A → B → D
# A → C → E → D

a = Node("A")
b = Node("B")
c = Node("C")
d = Node("D")
a.neighbors = [b, c]
b.neighbors = [d]
c.neighbors = [e]
e.neighbors = [d]


def shortest_path(start, target):
    # BFS to find the shortest path from start to target
    visited = {start}

    # Queue stores: (movie_node, path_of_movie_names)
    q = deque([(start, [start.data])])

    while q:
        movie, path = q.popleft()

        # Found the target
        if movie == target:
            return path

        for neighbor in movie.neighbors:
            # Mark as visited when we add it to the queue
            if neighbor not in visited:
                visited.add(neighbor)

                q.append(
                    (neighbor, path + [neighbor.data])
                )

    return None


print("shortest_path")
print(shortest_path(a, d) ) # True
print(shortest_path(b, c) ) # False




# Right now, every queue entry contains the entire path:

#(neighbor, path + [neighbor.data])

# So if the graph has a long path, we're repeatedly copying lists. A better approach is a parent map:

#A **parent map** stores, for each movie we discover, **which movie we came from** to reach it,
#so we don't have to carry the entire path in the queue. After BFS reaches the target, we follow the 
#parent pointers backward from the target to the start, then reverse that list to get the shortest path.
