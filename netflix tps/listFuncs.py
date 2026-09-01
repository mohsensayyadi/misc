students = [
    ("Alice", 90),
    ("Bob", 85),
    ("Charlie", 90),
    ("David", 75)
]

students.sort()

print(students)


students.sort(key=lambda x: x[1])

print(students)