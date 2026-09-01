# supose Netflix receives user ratings continuously and asks:

# “What is the median rating so far?”

# Use two heaps:

# max-heap        min-heap
#    lower half | upper half

# For example:

# 1  2  3 | 4  5  6
# max-heap | min-heap

# You keep the two halves balanced, and the median is available at the top of one or both heaps.


class MedianFinder:
    def __init__(self):
        self.lower_half = []  # max-heap (inverted min-heap)
        self.upper_half = []  # min-heap

    def addNum(self, num: int) -> None:
        import heapq
        
        # Add to max-heap (lower half)
        heapq.heappush(self.lower_half, -num)

        # Ensure the largest of lower_half is less than or equal to the smallest of upper_half
        if (self.lower_half and self.upper_half and 
            (-self.lower_half[0] > self.upper_half[0])):
            val = -heapq.heappop(self.lower_half)
            heapq.heappush(self.upper_half, val)

        # Balance the sizes of the two heaps
        if len(self.lower_half) > len(self.upper_half) + 1:
            val = -heapq.heappop(self.lower_half)
            heapq.heappush(self.upper_half, val)
        elif len(self.upper_half) > len(self.lower_half):
            val = heapq.heappop(self.upper_half)
            heapq.heappush(self.lower_half, -val)

    def findMedian(self) -> float:
        if len(self.lower_half) > len(self.upper_half):
            return -self.lower_half[0]
        else:
            return (-self.lower_half[0] + self.upper_half[0]) / 2.0