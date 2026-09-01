
# "Netflix wants to detect binge-watching sessions. Given a sorted list of timestamps (in minutes) 
# representing when a single user pressed 'play' on consecutive episodes, and a threshold gap (e.g. 15 minutes), 
# write a function that groups the timestamps into binge sessions — where a session continues as long as consecutive plays
# are within gap minutes of each other, and a new session starts once the gap is exceeded. Return the list of sessions
# (each as a list of timestamps), along with the length of the longest session."

# Example:

# timestamps = [0, 5, 12, 40, 45, 46, 90]
# gap = 15

#   Sessions:
#   [0, 5, 12]        (consecutive gaps: 5, 7 — both ≤ 15)
#   [40, 45, 46]       (gaps: 5, 1 — both ≤ 15; but 12->40 is a 28 gap, so new session starts)
#   [90]               (85 gap from 46 -> 90, so its own session)

# Longest session length: 3

class Sol:
    def __init__(self, timestamps=[], longest=0, win=0):
        self.timestamps = timestamps
        self.longest = 0
        self.sessions = []

    def find(self, gap):
        if not self.timestamps:
            return [], 0
        prev = self.timestamps[0]
        a = [prev]
        for ts in self.timestamps[1:]:
            d = ts - prev
            if d > gap:
                self.sessions.append(a)
                self.longest = max(self.longest, len(a))
                a = [ts]
            else:
                a.append(ts)
            prev = ts

        self.sessions.append(a)
        self.longest = max(self.longest, len(a))

        return self.sessions, self.longest

# test
sol = Sol([0, 5, 12, 40, 45, 46, 90])
sessions, longest = sol.find(15)
print("Sessions:", sessions)
print("Longest session length:", longest)