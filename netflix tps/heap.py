import heapq

a = [5, 2, 9, 1, 5, 6]

heapq.heapify(a)

print("Heapified list:", a)

for i in range(len(a)):
    print("Popped:", heapq.heappop(a))


def heap_sort(iterable):
    h = []
    for value in iterable: # O(n log n)
        heapq.heappush(h, value)
    return [heapq.heappop(h) for i in range(len(h))] # O(n log n)


o = heap_sort([5, 2, 9, 1, 5, 6])
print("Sorted in ascending order:", o)


def heap_sort_desc(iterable):
    h = []
    for value in iterable: # O(n log n)
        heapq.heappush(h, -value)
    return [-heapq.heappop(h) for i in range(len(h))] # O(n log n)


o = heap_sort_desc([5, 2, 9, 1, 5, 6])
print("Sorted in descending order:", o)
