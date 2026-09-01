# TPS Question: Key-Value Store
# Design a simple in-memory key-value store.
# Implement:
# put(key, value) — store or update a value.
# get(key) — return the value, or None if the key doesn't exist.
# delete(key) — remove the key and return whether it existed.
# Example:
# put("A", 10)
# put("B", 20)

# get("A")
# → 10

# put("A", 30)

# get("A")
# → 30

# delete("B")
# → True

# get("B")
# → None



# “Since I need fast lookup, insertion, update, and deletion by key, a HashMap is the natural data structure.

class KeyValueStore:
    def __init__(self):
        self.store = {}
    
    def put(self, key, value):
        self.store[key] = value

    def get(self, key):
        if key in self.store:
            return self.store[key]
        return None

    def delete(self, key):
        if key in self.store:
            del self.store[key]
            return True
        return False



kv = KeyValueStore()
kv.put("A", 10)
kv.put("B", 20)
print(kv.get("A"))  # → 10
kv.put("A", 30)
print(kv.get("A"))  # → 30



#  Follow up question 
# Modify the key-value store so that each key can have an expiration time, or TTL (time to live).
# For example:
# put("A", 100, 10)
# means "A" has value 100 and expires 10 seconds later.
# If we call get("A") after it expires, we should return None.


class KeyValueStoreWithTTL:
    def __init__(self):
        self.store = {}
    
    def put(self, key, value, ttl=None):
        expiration_time = None
        if ttl is not None:
            expiration_time = time.time() + ttl
        self.store[key] = (value, expiration_time)

    def get(self, key):
        if key in self.store:
            value, expiration_time = self.store[key]
            if expiration_time is None or time.time() < expiration_time:
                return value
            else:
                del self.store[key]  # Remove expired key
        return None

    def delete(self, key):
        if key in self.store:
            del self.store[key]
            return True
        return False

    

# Your solution uses lazy expiration:

# We only check whether a key has expired when someone calls get(key).

# So if "A" expires but nobody accesses it, it stays in the dictionary.

# The HashMap + min-heap solution is useful when we want to proactively or periodically
# clean up expired keys without checking every key.

# For this follow-up question, your solution is actually a great place to start in an 
# interview because it is simple and correct. Then, if the interviewer asks how to 
# efficiently clean up expired keys, you can introduce the min-heap.




import time
import heapq


class KeyValueStoreWithTTL2:

    def __init__(self):
        # HashMap:
        # key -> (value, expiration_time)
        self.store = {}

        # Min-heap:
        # (expiration_time, key)
        #
        # The key that expires earliest
        # is always at the top: self.expiry_heap[0]
        self.expiry_heap = []

    def put(self, key, value, ttl=None):

        # If ttl is None, the key never expires
        expiration_time = None

        if ttl is not None:
            # Calculate the absolute expiration time
            expiration_time = time.time() + ttl

            # Add expiration information to the min-heap
            heapq.heappush(
                self.expiry_heap,
                (expiration_time, key)
            )

        # Store the current value and expiration time
        self.store[key] = (value, expiration_time)

    def get(self, key):

        # Optional: clean up expired keys first
        self.cleanup()

        if key not in self.store:
            return None

        value, expiration_time = self.store[key]

        return value

    def delete(self, key):

        if key not in self.store:
            return False

        del self.store[key]
        return True

    def cleanup(self):

        current_time = time.time()

        # Look at the earliest expiration
        while (
            self.expiry_heap
            and self.expiry_heap[0][0] <= current_time
        ):

            # Remove the earliest-expiring entry
            expiration_time, key = heapq.heappop(
                self.expiry_heap
            )

            # Important:
            # The key may have been updated with a new TTL.
            # Only delete it if this heap entry still matches
            # the current expiration time.
            if key in self.store:
                value, current_expiration = self.store[key]

                if current_expiration == expiration_time:
                    del self.store[key]