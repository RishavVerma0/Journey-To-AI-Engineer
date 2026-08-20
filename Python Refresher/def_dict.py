from collections import defaultdict

students = [
    ("Ravi", "Python", 85),
    ("Aman", "Python", 92),
    ("Ravi", "SQL", 78),
    ("Aman", "SQL", 88),
    ("Neha", "Python", 95)
]

scores = defaultdict(list)

for name, subject, marks in students:
    scores[name].append(marks)

average = {
    name: sum(marks) / len(marks)
    for name, marks in scores.items()
}

result = sorted(
    average.items(),
    key=lambda x: x[1],
    reverse=True
)

print(result)