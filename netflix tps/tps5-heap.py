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
        self.counts = {} # HashMap to store movie counts  getCount("A") → 3

    def record(self, movie):
        if movie in self.counts:
            self.counts[movie] += 1
        else:
            self.counts[movie] = 1
    
    def getCount(self, movie):
        return self.counts[movie]
    

    def getTopK(self, k):
        # Use a min-heap to keep track of the top K movies
        # O(n log k) every time.
        min_heap = []
        for movie, count in self.counts.items():
            heapq.heappush(min_heap, (count, movie))
            if len(min_heap) > k:
                heapq.heappop(min_heap)
        
        # Extract the movies from the heap and sort them by count in descending order
        
        top_k_movies = sorted(min_heap, key=lambda x: (-x[0], x[1])) #  or min_heap.sort(key=lambda x: x[0], reverse=True)
        return [movie for count, movie in top_k_movies]

    

# What if getTopK(k) is called very frequently? Can you avoid rebuilding the heap every time?”

# The key change is: build and update the heap inside record(), so getTopK() doesn't scan all movies and rebuild a heap every time.



import heapq

class MovieTracker:
    def __init__(self, k):
        self.k = k

        # movie -> current count
        self.counts = {}

        # (count, movie)
        # Min-heap containing candidates for top K
        self.heap = []

    def record(self, movie):
        # Update the authoritative count
        self.counts[movie] = self.counts.get(movie, 0) + 1
        count = self.counts[movie]

        # Push the new version.
        # Older entries for this movie become stale.
        heapq.heappush(self.heap, (count, movie))

        # Keep the heap roughly bounded.
        if len(self.heap) > 2 * self.k:
            self._cleanup()

    def getCount(self, movie):
        return self.counts.get(movie, 0)

    def getTopK(self):
        # two-pass approach: pop from the heap until we have k valid entries, then push them back
        # lazy-update pattern: ignore stale entries in the heap, and only return valid ones
        result = []

        while self.heap and len(result) < self.k:
            count, movie = heapq.heappop(self.heap)

            # Ignore stale versions
            if self.counts[movie] != count:
                continue

            result.append((count, movie))

        # Put valid entries back
        for item in result:
            heapq.heappush(self.heap, item)

        result.sort(key=lambda x: (-x[0], x[1]))

        return [movie for count, movie in result]

    def _cleanup(self):
        # Remove stale entries
        new_heap = []

        while self.heap:
            count, movie = heapq.heappop(self.heap)

            if self.counts[movie] == count:
                new_heap.append((count, movie))

        for item in new_heap:
            heapq.heappush(self.heap, item)

