import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "notes.txt")

try:
    with open(file_path, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            if len(line) > 20:
                print(line)
except FileNotFoundError:
    print(f"Error: {file_path} was not found.")