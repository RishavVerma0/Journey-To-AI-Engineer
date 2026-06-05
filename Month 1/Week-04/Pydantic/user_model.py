# Install first:
# pip install pydantic

from pydantic import BaseModel, EmailStr, Field


# Define a data model
class User(BaseModel):
    # Required string field
    name: str

    # Email validation is automatic
    email: EmailStr

    # Age must be between 18 and 100
    age: int = Field(..., ge=18, le=100)

    # Optional field with a default value
    is_active: bool = True


try:
    # Create an object using incoming data
    user = User(
        name="John Doe",
        email="john@example.com",
        age=25
    )

    print("Valid user:")
    print(user)

except Exception as e:
    # If validation fails, Pydantic raises an error
    print("Validation error:")
    print(e)