import argparse

# Create parser
parser = argparse.ArgumentParser(description="Student Information")

# Add arguments
parser.add_argument("--name", type=str, required=True,
                    help="Enter student name")

parser.add_argument("--age", type=int, default=18,
                    help="Enter age")

parser.add_argument("--course",
                    choices=["Python", "Java", "C++"],
                    help="Select course")

parser.add_argument("--debug",
                    action="store_true",
                    help="Enable debug mode")

# Parse arguments
args = parser.parse_args()

# Print values
print("Name :", args.name)
print("Age :", args.age)
print("Course :", args.course)
print("Debug Mode :", args.debug)