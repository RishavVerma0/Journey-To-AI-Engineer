from contextlib import contextmanager
from pathlib import Path
@contextmanager
def file_manager(filename, mode):
    """
    Context manager for handling files safely."""
    
    file = open(filename, mode)

    try:
        print(f"Opening '{filename}'")
        yield file
    finally:
        file.close()
        print(f"Closing '{filename}'")

script_dir = Path(__file__).parent

file_path = script_dir / "Example.txt"

if __name__ == "__main__":
    with file_manager(file_path, "w") as file:
        file.write("Hello, Github!\n")
        file.write("This file was created using a custom context manager.")
