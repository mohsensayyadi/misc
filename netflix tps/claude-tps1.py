# ▎ "Our playback service should allow at most K start-playback requests per user per rolling 60-second window.
# Given requests in time order, decide which to allow or reject."

# Clarify: Rolling window vs. fixed buckets? Per-user isolation?
# What's the return — booleans, or the allowed list? Concurrency?
# Core: per-user deque of timestamps; evict entries older than the window. Discuss memory growth and cleanup.


class PlaybackLimiter:
    def __init__(self, k):
        self.k = k
        self.user_requests = {}  # user_id -> deque of timestamps

    def allow_request(self, user_id, timestamp):
        from collections import deque

        if user_id not in self.user_requests:
            self.user_requests[user_id] = deque()

        requests = self.user_requests[user_id]

        # Remove timestamps older than 60 seconds
        # not requests[-1] since it is not stack, it is a queue, so we need to check the front of the deque
        while requests and timestamp - requests[0] >= 60:
            requests.popleft()

        if len(requests) < self.k:
            requests.append(timestamp)
            return True  # Allow the request
        else:
            return False  # Reject the request



# my solution 

from collection import deque
class Sol:
    def __init__(self, k=0, win=0):
        self.d = {}
        self.k = k
        self.win = win

    def req(self, userId, ts):
        if userId not in self.d.keys():
            self.d[userId] = deque()

        q = self.d[userId]
        # lazy deletion
        while q and q[0] + self.win <= ts:
            q.popleft()

        # if q and q[0] + self.win > ts: # min: 10, cur_ts = 55, wind = 60
        if len(q) >= self.k:
            return False
        
        self.d[userId].append(ts) # space exists. add to q
        return True
