# Netflix maintains a “Recently Watched” list for each user.

# Design a data structure that supports:

# watch(movie)

# Moves the movie to the front of the recently watched list. If the movie is already in the list,
# remove it from its current position and move it to the front.

# Also support:

# getRecent(k)

# Returns the k most recently watched movies.

# For example:

# watch("A")
# watch("B")
# watch("C")
# watch("B")

# The list should be:

# B → C → A

# Then:

# getRecent(2)

# returns:

# ["B", "C"]
# Your challenge

# Try to design it so that:

# watch(movie) is O(1)
# getRecent(k) is O(k)

# Hint: This is a classic HashMap + doubly linked list problem.


class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class RecentlyWatched:
    def __init__(self):
        self.head = None
        self.tail = None
        self.movie_map = {}

    def watch(self, movie):
        if movie in self.movie_map:
            node = self.movie_map[movie]
            self._remove(node)
        else:
            node = Node(movie)
            self.movie_map[movie] = node

        self._add_to_front(node)

    def _remove(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        node.prev = None
        node.next = None

    def _add_to_front(self, node):
        node.prev = None
        node.next = self.head

        if self.head:
            self.head.prev = node
        else:
            self.tail = node

        self.head = node

    def getRecent(self, k):
        result = []
        current = self.head

        while current and len(result) < k:
            result.append(current.data)
            current = current.next

        return result