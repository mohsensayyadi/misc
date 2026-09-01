# Music Playlist History
# Design a MusicPlaylist storing (song, timestamp) plays: add, getAll sorted by timestamp (ties by insertion order), remove a single record, and removeAll records of a song.

# Problem Requirements
# We need to build a data structure that keeps a history of songs listened to. Each entry must store the song name and the timestamp when it was played.
# You need to create a class called MusicPlaylist with the following features:
# MusicPlaylist(): Sets up the playlist object.
# void add(String song, int timestamp): Saves a record that a specific song was played at a specific time.
# List<String> getAll(): Returns a list of all songs played.
# The list must be sorted by timestamp (earliest to latest).
# If two songs share the same timestamp, return them in the order they were originally added.
# boolean remove(String song, int timestamp): Deletes the record of a specific song played at a specific time.
# Returns true if the record existed and was deleted.
# Returns false if the record was not found.
# int removeAll(String song): Deletes every record of a specific song, no matter when it was played.
# Returns the total number of records deleted.

# Example Walkthrough
# Input Operations: ["MusicPlaylist", "add", "add", "add", "getAll", "remove", "getAll", "removeAll", "getAll"]
# Expected Output: [null, null, null, null, ["song1", "song2", "song1"], true, ["song1", "song1"], 2, []]
# Step-by-Step Explanation:
# // 1. Initialize the playlist
# MusicPlaylist playlist = new MusicPlaylist(); 

# // 2. Add songs with timestamps
# playlist.add("song1", 1); // Listen to song1 at time 1
# playlist.add("song2", 2); // Listen to song2 at time 2
# playlist.add("song1", 3); // Listen to song1 again at time 3

# // 3. Get all songs sorted by time
# playlist.getAll(); 
# // Returns ["song1", "song2", "song1"]

# // 4. Remove a specific record
# playlist.remove("song2", 2); // Remove song2 played at time 2
# // Returns true

# // 5. Check the list again
# playlist.getAll(); 
# // Returns ["song1", "song1"]

# // 6. Remove all instances of a song
# playlist.removeAll("song1"); // Remove all records of song1
# // Returns 2

# // 7. Check the list one last time
# playlist.getAll(); 
# // Returns []

# Input Limits
# Song Name Length: 1 <= song.length <= 100
# Timestamp Range: 0 <= timestamp <= 10^9
# Total Operations: At most 10^4 calls will be made to the methods (add, getAll, remove, and removeAll).
# Characters: Song names will only contain lowercase English letters and digits.





class MusicPlaylist:

    def __init__(self):
        # Store:
        # (timestamp, insertion_order, song)
        self.plays = []
        self.order = 0

    def add(self, song, timestamp):
        # Add a new play record
        self.plays.append((timestamp, self.order, song))
        self.order += 1

    def getAll(self):
        # Sort by timestamp first,
        # then insertion order for ties
        self.plays.sort(key=lambda x: (x[0], x[1]))

        # Return only song names
        return [song for timestamp, order, song in self.plays]

    def remove(self, song, timestamp):
        # Find the first matching record
        for i, (ts, order, s) in enumerate(self.plays):
            if s == song and ts == timestamp:
                self.plays.pop(i)
                return True

        return False

    def removeAll(self, song):
        # Remove all records for this song
        original_size = len(self.plays)

        self.plays = [
            record for record in self.plays
            if record[2] != song
        ]

        return original_size - len(self.plays)





#v2

# Let's modify the first implementation to address follow-up #1 and #6:

# #1: Make getAll() more efficient.
# #6: Make all operations efficient using multiple data structures.

# The key idea is to maintain:

# A HashMap for fast lookup by (song, timestamp).
# A sorted list of records for getAll().

# But there's a problem: inserting into a sorted Python list is still O(n). So for a truly efficient solution, 
# we'd want a balanced BST / sorted set, which Python doesn't provide natively.

# For a TPS interview, a very practical Python solution is to use a min-heap + HashMap, with lazy deletion.

import heapq


class MusicPlaylist:

    def __init__(self):
        # HashMap:
        # (song, timestamp) -> record
        self.records = {}

        # Min-heap:
        # (timestamp, insertion_order, song)
        self.heap = []

        self.order = 0

    def add(self, song, timestamp):
        record = (timestamp, self.order, song)

        # Fast lookup
        self.records[(song, timestamp)] = record

        # Keep records ordered by timestamp
        heapq.heappush(self.heap, record)

        self.order += 1

    def getAll(self):
        result = []

        # We cannot destroy the heap,
        # so make a temporary copy.
        temp = list(self.heap)
        heapq.heapify(temp)

        while temp:
            timestamp, order, song = heapq.heappop(temp)

            # Only include records that still exist
            if self.records.get((song, timestamp)) == (
                timestamp, order, song
            ):
                result.append(song)

        return result

    def remove(self, song, timestamp):
        key = (song, timestamp)

        if key not in self.records:
            return False

        # Remove from HashMap.
        # We leave the old entry in the heap.
        # It will be ignored later during getAll().
        del self.records[key]

        return True

    def removeAll(self, song):
        # Find all records for this song
        to_delete = []

        for key in self.records:
            if key[0] == song:
                to_delete.append(key)

        # Remove them from the HashMap
        for key in to_delete:
            del self.records[key]

        return len(to_delete)