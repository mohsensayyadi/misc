# TPS Question: Top-K Movie Engagement Scores

# Netflix has a stream of movie engagement scores arriving over time.

# Design a class MovieEngagement with:

# add(movie, score)

# Adds an engagement score for a movie.

# getTopK(k)

# Returns the K highest engagement scores, along with their movie names.

# Example:

# add("A", 80)
# add("B", 95)
# add("C", 70)
# add("D", 90)
# add("E", 100)

# Then:

# getTopK(3)
# → [("E", 100), ("B", 95), ("D", 90)]

import heapq
class MovieEngagement:
    def __init__(self):
        self.engagements = {} # HashMap

    
    def add(self, movie, score):
        # O(1) 
        if movie in self.engagements:
            self.engagements[movie] += score
        else:
            self.engagements[movie] = score


    def getTopK(self, k):
        # O(n log k) every time.
        h = []
        for movie, score in self.engagements.items():
            heapq.heappush(h, (score, movie)) # min-heap based on score
            if len(h) > k:
                heapq.heappop(h)
        # return [(movie, score) for score, movie in h]
        
        # Sort highest score first
        h.sort(key=lambda x: (-x[0], x[1]))

        return [(movie, score) for score, movie in h]


me = MovieEngagement()

me.add("A", 80)
me.add("B", 95)
me.add("C", 70)
me.add("D", 90)
me.add("E", 100)

print(me.getTopK(3)) # → [("E", 100), ("B", 95), ("D", 90)]


# What if getTopK(k) is called very frequently? Can you avoid scanning all movies and rebuilding the heap every time?

class MovieEngagement2:
    def __init__(self):
        self.engagements = {} # HashMap
        self.min_heap = [] # min-heap of size k
        self.k = 0

    
    def add(self, movie, score):
        # O(log k)
        if movie in self.engagements:
            self.engagements[movie] += score
        else:
            self.engagements[movie] = score
        
        # Update the min-heap if necessary
        if len(self.min_heap) < self.k:
            heapq.heappush(self.min_heap, (self.engagements[movie], movie))
        else:
            if self.engagements[movie] > self.min_heap[0][0]:
                heapq.heappop(self.min_heap)
                heapq.heappush(self.min_heap, (self.engagements[movie], movie))


    def getTopK(self, k):
        # O(k log k) to sort the heap contents
        self.k = k
        
        return sorted([(movie, score) for score, movie in self.min_heap], key=lambda x: (-x[1], x[0]))




import heapq

# use the lazy-update pattern
class MovieEngagement3:
    def __init__(self, k):
        self.engagements = {}
        self.heap = []
        self.k = k

    def add(self, movie, score):
        self.engagements[movie] = (
            self.engagements.get(movie, 0) + score
        )

        current_score = self.engagements[movie]

        # Push the newest score.
        # Older entries become stale.
        heapq.heappush(
            self.heap,
            (current_score, movie)
        )

        # Keep the heap from growing forever.
        # We may need extra cleanup because of stale entries.
        if len(self.heap) > 2 * self.k:
            self._cleanup()

    def _cleanup(self):
        # two-pass approach: pop from the heap until we have k valid entries, then push them back
        valid = []

        while self.heap:
            score, movie = heapq.heappop(self.heap)

            if self.engagements[movie] == score:
                valid.append((score, movie))

        for item in valid:
            heapq.heappush(self.heap, item)

    def getTopK(self):
        # two-pass approach: pop from the heap until we have k valid entries, then push them back
        result = []

        while self.heap and len(result) < self.k:
            score, movie = heapq.heappop(self.heap)

            if self.engagements[movie] != score:
                continue

            result.append((movie, score))

        for movie, score in result:
            heapq.heappush(self.heap, (score, movie))

        result.sort(key=lambda x: (-x[1], x[0]))

        return result



# handle stale heap entries correctly

import heapq

class MovieEngagement4:
    def __init__(self, k):
        self.engagements = {}
        self.heap = []
        self.k = k

    def add(self, movie, score):
        # Update the current score
        self.engagements[movie] = self.engagements.get(movie, 0) + score

        # Add the new score to the heap.
        # Any older entry for this movie is now stale.
        current_score = self.engagements[movie]
        heapq.heappush(self.heap, (current_score, movie))

    def getTopK(self):
        # first clean up stale entries from the heap - pop until we have k valid entries in a new list 
        # then push them back to the heap
        result = []

        while self.heap and len(result) < self.k:
            score, movie = heapq.heappop(self.heap)

            #. ******************* Stale entry: the movie's current score is different
            if self.engagements[movie] != score:
                continue

            # Current entry
            result.append((movie, score))

        # Put valid entries back for future calls
        for movie, score in result:
            heapq.heappush(self.heap, (score, movie))

        # Highest score first
        result.sort(key=lambda x: (-x[1], x[0]))

        return result