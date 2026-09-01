# Thread-safe Sliding Window P99 Latency Tracker
# Implement a thread-safe (concurrent) latency tracker that supports ingesting latency samples and querying the P99 
# over a recent time window.

# You need to implement two functions:

# setLatency(long timestamp, double latency)
# getP99Latency(long windowSize)
# 1) setLatency
# timestamp: the timestamp (integer) associated with this latency sample.
# latency: the latency value (double).
# This method may be called concurrently by multiple threads.
# 2) getP99Latency
# windowSize: size of the time window.
# Return the P99 (99th percentile) of the latency samples that fall within the most recent windowSize time range.
# This method may also be called concurrently, and concurrently with setLatency.
# P99 definition
# Sort the latencies in the window in ascending order.
# Let N be the number of samples in the window.
# Return the value at position ceil(0.99 * N) (1-indexed).
# Output convention
# If there is no data in the window, return an agreed value (e.g., 0.0 or NaN, as specified).
# Performance and concurrency requirements
# Must support high concurrency for reads/writes.
# Must control memory as data grows (evict samples outside the window).

# Example
# Assuming the window is [now - windowSize, now] (the exact definition of now should be clarified):

# Ingest:
# setLatency(1000, 10.0)
# setLatency(1005, 20.0)
# setLatency(1010, 30.0)
# Query:
# getP99Latency(20) computes the P99 over samples with timestamps in [now-20, now].
# Sample test scenarios
# Empty window: query P99 with no samples.
# Single sample: P99 equals that sample.
# Multiple samples: verify the ceil(0.99*N) rule.
# Window eviction: old samples must be excluded.
# Concurrent read/write: multiple threads calling both APIs; no exceptions and consistent behavior.


from collections import deque
from threading import RLock
import math


class LatencyTracker:
    def __init__(self, max_window):
        # Store: (timestamp, latency)
        self.samples = deque()

        # Latest timestamp we've received.
        self.latest_timestamp = None

        # Maximum amount of history we keep.
        self.max_window = max_window

        # Protects all shared state.
        self.lock = RLock()

    def setLatency(self, timestamp, latency):
        with self.lock:
            # Add the new sample
            self.samples.append((timestamp, latency))

            # Update "now"
            self.latest_timestamp = timestamp

            # Remove samples outside our maximum retention window.
            cutoff = timestamp - self.max_window

            while self.samples and self.samples[0][0] < cutoff:
                self.samples.popleft()

    def getP99Latency(self, windowSize):
        with self.lock:
            if self.latest_timestamp is None:
                return 0.0

            now = self.latest_timestamp
            cutoff = now - windowSize

            # Get latencies inside the requested time window.
            values = []

            for timestamp, latency in self.samples:
                if timestamp >= cutoff:
                    values.append(latency)

            if not values:
                return 0.0

            # Sort from smallest to largest.
            values.sort()

            n = len(values)

            # Problem definition:
            # position = ceil(0.99 * N), 1-indexed.
            index = math.ceil(0.99 * n) - 1

            return values[index]