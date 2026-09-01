# The Netflix home page has a list of shelves, each containing a number of titles. We want to deduplicate these titles
#  in the viewport (each shelf can display a maximum of X unique titles). Vertical scrolling can be ignored.

# Implement a function to deduplicate these titles:

# def dedupe_v5(titles: list[list[int]], x: int) -> list[list[int]]:
# This function should return a list where each element is a potentially deduplicated list.


# Parameters:

# titles: A list where each element is a list of titles on a shelf. Titles are represented by integers.
# x: Maximum number of unique titles that can be displayed in the viewport per shelf.
# Example:

# >>> dedupe_v5([[1, 2, 2, 3, 4], [1, 2, 5, 6, 4]], 3)
# [[1, 2, 3, 4], [5, 6, 4]]

# >>> dedupe_v5([[5, 5, 1, 2], [1, 1, 1, 2, 3]], 1)
# [[5], [1, 2, 3]]
# Constraints:

# 1 <= x <= 100
# 1 <= titles[i].length <= 100
# 1 <= titles[i][j] <= 1000


def dedupe_v5(titles: list[list[int]], x: int) -> list[list[int]]:
    result = []

    for shelf in titles:
        seen = set()
        unique = []

        for title in shelf:
            if title not in seen:
                seen.add(title)
                unique.append(title)

                if len(unique) == x:
                    break

        result.append(unique)

    return result




# find the length of the longest continuous sublist without duplicates, solvable by a sliding window.

class NetflixShelves:

    def dedupe(self, titles, x):
        """
        Remove duplicates within each shelf.
        Keep at most x unique titles per shelf.
        Preserve the original order.
        """
        result = []

        for shelf in titles:
            seen = set()
            unique = []

            for title in shelf:
                if title not in seen:
                    seen.add(title)
                    unique.append(title)

                    if len(unique) == x:
                        break

            result.append(unique)

        return result

    def longest_unique(self, titles):
        """
        For each shelf, find the length of the longest
        continuous sublist without duplicates.
        """
        result = []

        for shelf in titles:
            seen = set()
            left = 0
            best = 0

            for right in range(len(shelf)):
                while shelf[right] in seen:
                    seen.remove(shelf[left])
                    left += 1

                seen.add(shelf[right])
                best = max(best, right - left + 1)

            result.append(best)

        return result


# Global dedup: a show name must not appear in multiple rows (keep it in the earliest row where it first appears; 
# skip occurrences in later rows).
    def dedupe(self, titles):
        seen = set()
        result = []

        for shelf in titles:
            new_shelf = []

            for title in shelf:
                # Handles both:
                # 1. duplicate within this shelf
                # 2. title already seen in an earlier shelf
                if title in seen:
                    continue

                seen.add(title)
                new_shelf.append(title)

            result.append(new_shelf)

        return result