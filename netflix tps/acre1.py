# Problem: Weighted Cache Eviction (Weight-Constrained Cache)
# Design and implement a cache `WeightedCache` with a total weight capacity constraint.
# Each cache entry has:

# * `key`
# * `value`
# * `weight` (a positive integer)

# Given `capacity`, the sum of weights of all cached entries must not exceed `capacity`.
# If an insert/update makes the total weight exceed `capacity`, evict entries as follows:

# * Repeatedly evict the entry with the largest weight until the total weight is within `capacity`.
# * If multiple entries share the same maximum weight, any deterministic tie-breaking rule is acceptable.

# Supported operations:

# 1. `get(key) -> value`
#    * Return the value if present, otherwise `-1`.
# 2. `put(key, value, weight) -> void`
#    * If `key` exists, update its `value` and `weight`.
#    * Otherwise insert a new entry.
#    * After insert/update, evict as needed.
#    * If `weight > capacity`, the item cannot be cached (recommended behavior: ignore the `put`).

# Constraints / Expectations

# * `capacity >= 1`
# * `weight >= 1`
# * Aim for efficient operations (e.g., close to `O(log n)`).

# Example

# * `capacity = 10`
# * `put(A, 1, 6)` -> `{A(6)}` total 6
# * `put(B, 2, 5)` -> total 11, evict heaviest `A(6)`, remaining `{B(5)}`
# * `get(A) -> -1`
# * `get(B) -> 2`

# I/O Format for Testing

# * Line 1: `capacity`
# * Line 2: `q` number of operations
# * Next `q` lines:
#    * `PUT key value weight`
#    * `GET key`

# Print one line per `GET`.

import heapq


class WeightedCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = {}       # key -> [value, weight, rowId]
        self.heap = []       # (-weight, rowId, key)
        self.total_weight = 0
        # why keep it anyway? Not for staleness — for heap comparability. heapq compares tuples element-by-element.
        #  If two entries tie on -weight (the first element), Python falls through to comparing the second element to break the tie.
        #  Without rowId, that second element is the key itself — and as the test above shows,
        # the moment two different keys with equal weight are of incomparable types (e.g., one string key, one int key), 
        # heapq crashes with a TypeError
        self.rowId = 0     

    def get(self, key):
        if key not in self.data:
            return -1
        return self.data[key][0]

    def put(self, key, value, weight):
        if weight > self.capacity:
            return

        if key in self.data:
            self.total_weight -= self.data[key][1]

        self.rowId += 1
        self.data[key] = [value, weight, self.rowId]
        self.total_weight += weight
        heapq.heappush(self.heap, (-weight, self.rowId, key))

        # Evict entries until total weight is within capacity
        # lazy del
        while self.total_weight > self.capacity:
            neg_w, id, k = heapq.heappop(self.heap)
            if k in self.data and self.data[k][1] == -neg_w and self.data[k][2] == id:
                self.total_weight -= self.data[k][1]
                del self.data[k]
            # else ignore the stale entry.


# test
