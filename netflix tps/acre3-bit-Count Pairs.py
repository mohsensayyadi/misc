
# # Problem: Count Pairs of Show Names with No Common Characters
# Given a list of show names shows (array of strings). For a pair of indices (i, j) with 0 <= i < j < N, 
# the pair is valid if shows[i] and shows[j] share no common character.

# Return the number of valid pairs.

# Character Set
# Show names contain only lowercase letters a-z.
# Input Format
# Line 1: integer N
# Line 2: N space-separated show names
# Output Format
# Print one integer: the number of valid pairs
# Constraints
# 1 <= N <= 2e5
# Each name length: 1..50
# Sample Tests
# Test 1 Input:

# 4
# ab cd a bcd
# Output:

# 2
# Test 2 Input:

# 3
# a aa aaa
# Output:

# 0
# Test 3 Input:

# 5
# a b c d e
# Output:

# 10
# Test 4 Input:

# 4
# abc def ghi jkl
# Output:

# 6
# Test 5 Input:

# 6
# ab ac ad ae af ag
# Output:

# 0

def count_valid_pairs(shows):
    masks = []

    for show in shows:
        # 26-element binary array
        chars = [0] * 26

        for ch in show:
            index = ord(ch) - ord('a')
            chars[index] = 1

        # Convert the binary array to an integer
        mask = int("".join(map(str, chars)), 2)
        masks.append(mask)

    result = 0

    # Compare every pair of shows
    for i in range(len(masks)):
        for j in range(i + 1, len(masks)):
            # AND == 0 means no common characters
            if masks[i] & masks[j] == 0:
                result += 1

    return result


# Can we make it more efficient?

# Yes. The main optimization is to notice that there are only 26 characters, so many shows can have the same character mask.

# Instead of comparing every pair of the n shows, we can count how many times each mask occurs.

from collections import Counter

def count_valid_pairs(shows):
    # O(n * L + M²)
    # where L ≤ 50 is the maximum show length and M is the number of distinct character masks.
    # The crucial point is that:M ≤ 2²⁶
    # because there are only 26 possible characters. In practice, M can be much smaller than n.
    freq = Counter()

    # Build one 26-character mask for each show
    for show in shows:
        chars = [0] * 26

        for ch in set(show):
            chars[ord(ch) - ord('a')] = 1

        mask = int("".join(map(str, chars)), 2)
        freq[mask] += 1

    masks = list(freq)
    result = 0

    # Compare distinct masks instead of all N shows
    for i in range(len(masks)):
        for j in range(i + 1, len(masks)):
            if masks[i] & masks[j] == 0:
                # Every show with mask i can pair with
                # every show with mask j.
                result += freq[masks[i]] * freq[masks[j]]

    return result   