# Question: Merge Two Sorted Feeds

# LinkedIn has two sorted feeds of posts, where each post is ordered by timestamp from newest to oldest.

# Given two linked lists:

# Feed 1: 10 → 7 → 3
# Feed 2: 9 → 8 → 2

# Merge them into one sorted feed:

# 10 → 9 → 8 → 7 → 3 → 2

# Implement:

# mergeFeeds(feed1, feed2)


def mergeFeeds(feed1, feed2):
    dummy = Node(0)
    current = dummy

    while feed1 and feed2:
        if feed1.data > feed2.data:
            current.next = feed1
            feed1 = feed1.next
        else:
            current.next = feed2
            feed2 = feed2.next
        current = current.next

    if feed1:
        current.next = feed1
    elif feed2:
        current.next = feed2

    return dummy.next


# What if the feeds are sorted from oldest to newest instead?


def mergeFeedsOldestToNewest(feed1, feed2):
    dummy = Node(0)
    current = dummy

    while feed1 and feed2:
        if feed1.data < feed2.data:
            current.next = feed1
            feed1 = feed1.next
        else:
            current.next = feed2
            feed2 = feed2.next
        current = current.next

    if feed1:
        current.next = feed1
    elif feed2:
        current.next = feed2

    return dummy.next



# A very natural TPS follow-up is:

# What if LinkedIn has K sorted feeds instead of just two? Merge all K feeds into one sorted feed.


import heapq


def merge_k_feeds(feeds):
    heap = []

    # Put the first node from each non-empty feed into the heap
    for i, node in enumerate(feeds):
        if node:
            heapq.heappush(heap, (node.data, i, node))

    dummy = Node(0)
    current = dummy

    while heap:
        _, i, node = heapq.heappop(heap)

        # Reuse the existing node
        current.next = node
        current = current.next

        # Add the next node from the same feed
        if node.next:
            heapq.heappush(
                heap,
                (node.next.data, i, node.next)
            )

    return dummy.next