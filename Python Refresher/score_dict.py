import random

scores = {f"Student{i}": random.randint(60, 100) for i in range(1, 201)}

max_score = max(scores, key=scores.get) # type: ignore

print(max_score)          # Student with the highest score
print(scores[max_score])  # Their score