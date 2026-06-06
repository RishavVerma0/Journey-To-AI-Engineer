import os

# Read environment variables
app_name = os.getenv("APP_NAME", "My Application")
port = os.getenv("PORT", "5000")
debug = os.getenv("DEBUG", "False")

print("Application Settings")
print("--------------------")
print("App Name:", app_name)
print("Port:", port)
print("Debug:", debug)

# Set a new variable
os.environ["CURRENT_USER"] = "Student"

print("\nNew Variable:")
print("Current User:", os.getenv("CURRENT_USER"))