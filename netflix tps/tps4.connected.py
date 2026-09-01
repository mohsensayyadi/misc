# TPS Question: Find Connected Movies

# Suppose Netflix has a graph where movies are connected when they are related.

# Design a function:

# connected_movies(start)

# that returns all movies reachable from a given movie.

# For example:

# A → B → D
# ↓
# C → E  F J


class Node:
    def __init__(self, data):
        self.data = data
        self.neighbors = []


a = Node("A")
b = Node("B")
c = Node("C")
d = Node("D")
e = Node("E")
f = Node("F")
j = Node("J")

a.neighbors = [b, c]
b.neighbors = [d]
c.neighbors = [e]


def connected_movies(start):
    visited = set()

    result = []
    st = [start]
    visited.add(start)
    while st:
        movie = st.pop()
        
        for neighbor in movie.neighbors:
            if neighbor in visited:
                continue
            st.append(neighbor)
            visited.add(neighbor)
        result.append(movie.data)
    return result
        

print(connected_movies(a))  # Output: ['A', 'C', 'E', 'B', 'D'] or any order of these movies



# Now, instead of returning all movies reachable from start, return the number of connected components in the entire graph

all_movies = [a, b, c, d, e, f, j]
def count_connected_components(all_movies):
    # because the DFS runs do not overlap. Finding connected components using BFS/DFS = O(V + E)
    visited = set()
    count = 0

    
    for movie in all_movies:
        if movie in visited:
            continue
        count += 1
        st = [movie]
        visited.add(movie)
        while st:
            movie_popped = st.pop()
            
            for neighbor in movie_popped.neighbors:
                if neighbor in visited:
                    continue
                st.append(neighbor)
                visited.add(neighbor)
    return count

count = count_connected_components(all_movies)
print(count)  # Output: 2, since there are two connected components: {A, B, C, D, E} and {F}




# Can you find the largest connected component?


def largest_connected_component(all_movies):
    visited = set()
    largest_size = 0

    for movie in all_movies:
        if movie in visited:
            continue
        size = 0
        st = [movie]
        visited.add(movie)
        while st:
            movie_popped = st.pop()
            size += 1
            
            for neighbor in movie_popped.neighbors:
                if neighbor in visited:
                    continue
                st.append(neighbor)
                visited.add(neighbor)
        largest_size = max(largest_size, size)
    return largest_sizebnvgicvbdl
    