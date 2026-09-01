# TPS-Style Question: Remove a Movie in O(1)

# Netflix maintains a collection of recently viewed movies using a doubly linked list:

# A ⇄ B ⇄ C ⇄ D ⇄ E

# You need to support:

# remove(movie)

# The requirement is that remove(movie) must run in O(1) time.

# For example:

# remove("C")

# should produce:

# A ⇄ B ⇄ D ⇄ E
# Constraints

# You may not traverse the linked list to find "C".

# Design the data structure and implement:

# remove(movie)

# in O(1).

# Hint

# Think about combining:

# HashMap + Doubly Linked List

# The HashMap should let you go directly from:

# " C " → Node(C)



# notes : implement helper functions for doubly linked list in the class RecentlyWatched.
# You can use them to implement remove(movie) in O(1) time.

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class RecentlyWatched:
    def __init__(self):
        # hashmap for O(1) access to nodes by movie name, two pointers for head and tail of the doubly linked list
        self.head = None
        self.tail = None
        self.movie_map = {}

    def watch(self, movie):
        # If the movie is already in the list, remove it from its current position and move it to the front.
        if movie in self.movie_map:
            node = self.movie_map[movie]
            self._remove(node)
        else:
            node = Node(movie)
            self.movie_map[movie] = node
        
        self._add_to_front(node)

    
    def _remove(self, node):
        # Remove the node from the doubly linked list
        
        # update the previous node's next pointer
        # If the node is the head, we need to update the head pointer
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        
        # update the next node's prev pointer
        # If the node is the tail, we need to update the tail pointer
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        

    def _add_to_front(self, node):
        # Add the node to the front of the doubly linked list
        node.prev = None
        node.next = self.head
        
        if self.head:
            self.head.prev = node
        else:
            self.tail = node
        
        self.head = node

    def remove(self, movie):
        # Remove the movie from the list in O(1) time
        if movie in self.movie_map:
            node = self.movie_map[movie]
            self._remove(node)
            del self.movie_map[movie]



    # follow-up question?: Can you also support moveToFront(movie) in O(1)?”
    def moveToFront(self, movie):
        # Move the movie to the front of the list in O(1) time
        if movie in self.movie_map:
            node = self.movie_map[movie]
            self._remove(node)
            self._add_to_front(node)

