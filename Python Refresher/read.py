from pathlib import Path

try:
    with open(Path(__file__).parent / "notes.txt") as f:
        for line in f:
            if len(line.strip()) > 20:
                print(line.strip())
except FileNotFoundError:
    print("notes.txt not found.")