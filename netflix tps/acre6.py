# Problem: Top Title Selection Service with “No Immediate Repeat” Rotation
# Implement a service that selects one movie/show title to display on a user’s homepage billboard.
#  The system maintains a relevance score score for each title_id.

# You must support two APIs:

# upsertTitleScore(title_id: str, score: float): Insert a new title or update an existing title’s score.
# getTopTitle() -> str: Return the title_id that should be displayed now.
# Requirements
# Higher score has priority: Among available titles, the service should prefer returning the title with the highest score.
# Avoid immediate repeats: If there exists any other selectable title, getTopTitle() should not return the same title_id in two consecutive calls.
# Titles can reappear: After a title is returned, it may be returned again in later calls (subject to rules 1 and 2).
# Single-title case: If the system contains only one title, it may be returned repeatedly.
# Repeated upserts: upsertTitleScore may be called multiple times for the same title_id; the score must be updated correctly.
# Expectations
# Explain your data structure choices and implement both APIs.
# Handle how score updates affect subsequent getTopTitle() results.
# Discuss time/space complexity goals for upsert and getTopTitle.
# Examples (illustrative)
# Start: upsert(A, 10), upsert(B, 9)
# First getTopTitle() returns A
# Second call should return B (no immediate repeat of A)
# Third call may return A again
# Start: upsert(A, 10)
# Repeated getTopTitle() calls can keep returning A
# Test Cases (stdin/stdout style)
# Use GET for getTopTitle() and UPSERT id score for upsertTitleScore.

# Two-title rotation
# input
# UPSERT A 10
# UPSERT B 9
# GET
# GET
# GET
# GET
# output (one valid output)
# A
# B
# A
# B
# Single title repeats
# input
# UPSERT A 10
# GET
# GET
# GET
# output
# A
# A
# A
# Upsert update changes ordering
# input
# UPSERT A 10
# UPSERT B 9
# GET
# UPSERT B 100
# GET
# GET
# output (must prioritize B after the update and avoid immediate repeats)
# A
# B
# A
# Three titles; avoid immediate repeats and prefer the highest
# input
# UPSERT A 10
# UPSERT B 9
# UPSERT C 8
# GET
# GET
# GET
# GET
# GET
# output (one valid output)
# A
# B
# A
# B
# A
# Ties (you may define a deterministic tie-break rule)
# input
# UPSERT A 10
# UPSERT B 10
# GET
# GET
# GET
# output (example)
# A
# B
# A

import heapq


class TopTitleService:
    def __init__(self):
        # title_id -> current score
        self.scores = {}

        # title_id -> latest version number
        self.versions = {}

        # Max-heap using negative scores:
        # (-score, title_id, version)
        self.heap = []

        # Title returned by the previous getTopTitle()
        self.last_title = None

    def upsertTitleScore(self, title_id, score):
        # O(log n)
        # Update the current score
        self.scores[title_id] = score

        # Increase version so old heap entries become stale
        version = self.versions.get(title_id, 0) + 1
        self.versions[title_id] = version

        # Add the new version to the heap
        heapq.heappush(
            self.heap,
            (-score, title_id, version)
        )

    def _is_valid(self, entry):
        neg_score, title_id, version = entry

        # Ignore old heap entries created before a score update
        return (
            title_id in self.scores
            and self.versions[title_id] == version
        )

    def getTopTitle(self):
        # O(log n)
        if not self.scores:
            return ""

        skipped = []

        # Find the best valid title that isn't the previous title
        while self.heap:
            entry = heapq.heappop(self.heap)

            if not self._is_valid(entry):
                # Stale entry
                continue

            neg_score, title_id, version = entry

            if title_id != self.last_title:
                # Put skipped valid entries back
                for item in skipped:
                    heapq.heappush(self.heap, item)

                # Put this title back too, because titles can reappear
                heapq.heappush(self.heap, entry)

                self.last_title = title_id
                return title_id

            # This is the previous title.
            # Keep it aside while we look for the next-best title.
            skipped.append(entry)

        # If we got here, there was no other valid title.
        # Therefore the previous title is the only selectable title.
        for item in skipped:
            heapq.heappush(self.heap, item)

        self.last_title = skipped[0][1]
        return self.last_title