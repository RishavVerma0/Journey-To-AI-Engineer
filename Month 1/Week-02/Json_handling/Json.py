#Import python's built-in Json Module
import json

# ---------------------------------------------------
# PYTHON DICTIONARY (Normal Python object)
# ---------------------------------------------------

user = {
    "first-name" : "Rishav",
    "last-name" : "Verma",
    "age" : 22,
    "Skills" : ["Python", "Java", "C++"],
    "Education" : {"Bachelors" : "Computer Science"},
}

# Python dictionary:
print("Python Dictionary")
print(user)

print("\n")

# ---------------------------------------------------
# CONVERT PYTHON OBJECT -> JSON STRING
# json.dumps() = dictionary to JSON string
# ---------------------------------------------------
json_data = json.dumps(user, indent=4)

print("Converted into JSON String:")
print(json_data)

print("\n")
# ---------------------------------------------------
# CONVERT JSON STRING -> PYTHON OBJECT
# json.loads() = JSON string to dictionary
# ---------------------------------------------------

python_obj = json.loads(json_data)
print("Converted back to Python Dictionary:")
print(python_obj)

print("\n")

# ---------------------------------------------------
# ACCESSING VALUES
# ---------------------------------------------------

print("User Name:" , python_obj["first-name"]+ " " + python_obj["last-name"])
print("Age of the user is : " ,python_obj["age"])
print("Skills of the user are : ", python_obj["Skills"])

print("\n")



# ---------------------------------------------------
# WRITING JSON TO A FILE
# json.dump() writes directly into a file
# ---------------------------------------------------

with open("user.json", "w") as f:
    json.dump(user, f, indent=4)

print("JSON data written to student.json")

print("\n")

# ---------------------------------------------------

# READING JSON FROM A FILE

# json.load() reads JSON from a file

# ---------------------------------------------------

with open("user.json", "r") as file:

    data = json.load(file)

print("JSON data read from file:")

print(data)

print("\n")

# ---------------------------------------------------

# ERROR HANDLING FOR INVALID JSON

# ---------------------------------------------------

invalid_json = '{"name": "Aman", age: 22}'  

# ERROR because age key is missing double quotes

try:

    obj = json.loads(invalid_json)

except json.JSONDecodeError as e:

    print("Invalid JSON Detected!")

    print("Error:", e)