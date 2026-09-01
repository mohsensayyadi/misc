# Part 1: Detect duplicate episodes
# Given a list episodes of episode IDs in a user's watch history (in watch order), 
# determine whether any episode ID appears more than once.

# Return True if there is any duplicate ID
# Otherwise return False
# Examples
# episodes = [55, 66, 77, 88, 99] → False
# episodes = [55, 66, 77, 88, 66] → True
# Constraints
# 1 <= len(episodes) <= 2e5
# 0 <= episodes[i] <= 1e9


# Part 2: Rewatch the same episode within K days
# You are given a list of watch events events, each containing:

# day: an integer day index when the watch happened (multiple watches may occur on the same day)
# episode_id: the episode ID
# Determine whether there exists an episode_id such that the user watched that same episode at least twice
#  within some window of length K days (i.e., for two events, |day_i - day_j| <= K).

# Return True if such a pair exists, otherwise False.

# Input format (for implementation/testing)
# First line: n K
# Next n lines: day episode_id
# Sample tests
# Input:

# 5 3

# 1 66
# 2 77
# 4 66
# 10 66
# 11 88
# Output:

# True
# Explanation: episode 66 was watched on day 1 and day 4 (difference 3 <= K).

# Input:

# 4 2
# 1 66
# 4 66
# 7 66
# 10 66
# Output:

# False
# Constraints
# 1 <= n <= 2e5
# 0 <= day <= 1e9
# 1 <= K <= 1e9


# Part 3: Watch at least two episodes from the same season within K days
# You are given the same watch events list events (day, episode_id). Determine whether there exists a window of length K days in which the user watched
#  at least two episodes from the same season.

# Season rule: two episodes are considered from the same season if their episode IDs differ by at most T.

# Formally, check whether there exist two events i, j such that:

# |day_i - day_j| <= K (time window constraint)
# |episode_id_i - episode_id_j| <= T (same-season constraint)
# Return True if such a pair exists, otherwise False.

# Input format (for implementation/testing)
# First line: n K T
# Next n lines: day episode_id
# Sample tests
# Input:

# 5 7 2
# 1 100
# 3 105
# 5 101
# 20 200
# 21 300
# Output:

# True
# Explanation: episode 100 (day 1) and 101 (day 5) are within K=7 days and within T=2 IDs.

# Input:

# 4 3 1
# 1 100
# 5 101
# 9 102
# 12 103
# Output:

# False
# Constraints
# 1 <= n <= 2e5
# 0 <= day <= 1e9
# 0 <= episode_id <= 1e9
# 1 <= K <= 1e9
# 0 <= T <= 1e9

# Part 1 — Detect duplicate episodes
class Solution:
    def hasDuplicate(self, episodes):
        seen = set()

        for episode in episodes:
            if episode in seen:
                return True

            seen.add(episode)

        return False


# part2
# Determine whether there exists an episode_id such that the user watched that same episode at least twice
#  within some window of length K days (i.e., for two events, |day_i - day_j| <= K).
from collections import defaultdict, deque


class Solution:
    def rewatchedWithinK(self, events, K):
        # episode_id -> deque of recent watch days
        watches = defaultdict(deque)

        for day, episode in events:
            q = watches[episode]

            # Remove watches that are more than K days old
            while q and day - q[0] > K:
                q.popleft()

            # If there is still a previous watch,
            # it is within K days of the current watch.
            if q:
                return True

            q.append(day)

        return False
# With `K = 3`, suppose we have `day 1 → episode 66`, `day 2 → episode 77`, and `day 4 → episode 66`. When we process day 1,
#  the queue for episode 66 is empty, so we add `1`. When we process day 2, the queue for episode 77 is empty, so we add `2`. 
# When we reach day 4 for episode 66, the queue already contains the previous watch `[1]`; since `4 - 1 = 3`, which is within `K = 3`, we immediately return `True`. We check the queue **before** adding the current timestamp because we're looking for a previous occurrence within the allowed window; if we added the current timestamp first, we'd always find the current event itself and incorrectly return `True`.



# part3
# |day_i - day_j| <= K (time window constraint)
# |episode_id_i - episode_id_j| <= T (same-season constraint)
# Return True if such a pair exists, otherwise False.
class Solution:
    def sameSeasonWithinK(self, events, K, T):
        # This version is O(n²) in the worst case
        # Sort events by day
        events.sort(key=lambda x: x[0])

        window = []
        left = 0

        for right in range(len(events)):
            day, episode = events[right]

            # Remove events that are too old
            while day - events[left][0] > K:
                old_episode = events[left][1]

                # Remove old episode from window
                window.remove(old_episode)

                left += 1

            # Check whether any existing episode ID
            # is within T of the current episode.
            for old_episode in window:
                if abs(old_episode - episode) <= T:
                    return True

            # Add current episode
            window.append(episode)

        return False