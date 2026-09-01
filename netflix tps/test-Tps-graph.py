# Given a starting movie and a number K, find all movies that are within K connections of the
# starting movie.

# For example:

#        B ─── D
#       /
# A ───
#       \
#        C ─── E ─── F  J


# Starting from A with K = 2:

# Distance 0: A
# Distance 1: B, C
# Distance 2: D, E

class Node():
    def __init__(self, val=0):
        self.val = val
        self.neighbors = []

from collections import deque

def bfs(node, k):
    q = deque([(node, 0)])
    o = []
    seen = set()
    seen.add(node)

    while len(q) >0:
        n, dist = q.popleft()
        if dist ==k:
            o.append(n.val)
        else:
            for ne in n.neighbors: # and dist <k
                if ne not in seen:
                    q.append((ne, dist+1) )
                    seen.add(ne)
        
    return o



a = Node("A")
b = Node("B")
c = Node("C")
d = Node("D")
e = Node("E")
f = Node("F")
j = Node("J")

a.neighbors = [b, c]
b.neighbors = [a, d]
c.neighbors = [a, e]
d.neighbors = [b]
e.neighbors = [c, f]
f.neighbors = [e]
j.neighbors = []

aa= bfs(a, 1)
print(aa) # → [D, E] or [E, D] (order doesn't matter)



# Now, instead of returning all movies reachable from start, return the number of connected components in the entire graph

def count_connected_components(nodes):
    c = 0 
    seen = set()
    for node in nodes:
        # print("node", node.val)
        if node in seen:
            continue
        c +=1
        q = deque([node])
        seen.add(node)

        while len(q) >0:
            n = q.popleft()
            for ne in n.neighbors:
                if ne not in seen:
                    q.append(ne )
                    seen.add(ne)
        
    print("count_connected_components", c)
    return c


count_connected_components([a, b, c, d, e, f, j]) # → 1