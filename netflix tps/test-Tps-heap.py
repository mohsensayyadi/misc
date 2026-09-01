# TPS Question: Top-K Most Watched Movies

# Netflix wants to identify its most popular movies.
# Design a MovieTracker that supports:

# record(movie) — records one additional watch for a movie.
# getCount(movie) — returns how many times the movie has been watched.
# getTopK(k) — returns the K most-watched movies.

# Example:
# record("A")
# record("B")
# record("A")
# record("C")
# record("A")
# record("B")

# Then:

# getCount("A") → 3
# getCount("B") → 2


# getTopK(2) → ["A", "B"]

import heapq
class MovieTracker:
    def __init__(self):
        self.h = {}

    
    def record(self, mov):
        if mov in self.h.keys():
            self.h[mov] +=1
        else:
            self.h [mov]= 1
    
    def getCount(self, mov):
        if mov in self.h.keys():
            return self.h[mov]
        else:
            return 0
    

    def getTopK(self, k):
        # time complexity: O(n log n) every time.
        # space complexity: O(n)
        a = []
        # heapq.heapify(a)

        o = []
        for mov, c in self.h.items():
            heapq.heappush(a, (-c, mov))

        while len(o) < k:
            c, mov = heapq.heappop(a)
            o.append( (mov, -c) )
        
        return o


m = MovieTracker()


m.record("A")
m.record("B")
m.record("A")
m.record("C")
m.record("A")
m.record("B")

print(m.getCount("A")) # → 3

print(m.getTopK(2) ) # → ["A", "B"])



# For the more efficient Top-K pattern we discussed, you'd maintain a min-heap of only K movies, giving:

# getTopK(k) → O(n log k)


    def getTopK(self, k):
        a = []
        # heapq.heapify(a)

        o = []
        for mov, c in self.h.items():
            if len(a) < k:
                heapq.heappush(a, (c, mov))
            else:
                heapq.heappushpop(a, (c, mov))

        while len(o) < k:
            c, mov = heapq.heappop(a)
            o.append((mov, c))
         
        o.reverse()
        return o