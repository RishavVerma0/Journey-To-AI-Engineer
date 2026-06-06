import os


def get_env_variable(var_name, default=None, required=False):
    """
    Read an environment variable safely.

    Parameters:
        var_name (str): Name of the environment variable
        default: Value to return if variable is missing
        required (bool): Raise an error if variable is missing

    Returns:
        str: Environment variable value
    """

    value = os.getenv(var_name, default)

    # Check if a required variable is missing
    if required and value is None:
        raise ValueError(
            f"Required environment variable '{var_name}' is not set."
        )

    return value


# -------------------------------
# Load application configuration
# -------------------------------

try:
    API_KEY = get_env_variable(
        "API_KEY",
        required=True
    )

    DB_HOST = get_env_variable(
        "DB_HOST",
        required=True
    )

    DB_PORT = get_env_variable(
        "DB_PORT",
        default="5432"
    )

    DEBUG = (
        get_env_variable(
            "DEBUG",
            default="False"
        ) or "False"
    ).lower() == "true"

except ValueError as error:
    print("Configuration Error:", error)
    exit()


# -------------------------------
# Display loaded configuration
# -------------------------------

print("Application Configuration")
print("-" * 30)

# Hide most of the API key for security
print("API Key:", API_KEY[:4] + "****" if API_KEY else "Not set")

print("Database Host:", DB_HOST)
print("Database Port:", DB_PORT)
print("Debug Mode:", DEBUG)


# -------------------------------
# Simulated application startup
# -------------------------------

if DEBUG:
    print("\nRunning in DEVELOPMENT mode")
else:
    print("\nRunning in PRODUCTION mode")

print("Connecting to database...")
print(f"Connected to {DB_HOST}:{DB_PORT}")

# Linux/macOS
# export API_KEY=sk_test_123456
# export DB_HOST=localhost
# export DB_PORT=5432
# export DEBUG=True