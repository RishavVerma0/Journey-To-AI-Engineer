from fastapi import FastAPI

app = FastAPI()

# GET Route
@app.get("/")
def home():
    return {"message": "Welcome to FastAPI"}

# Path Parameter Route
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

# Query Parameter Route
@app.get("/search")
def search(q: str):
    return {"search_term": q}

# POST Route
@app.post("/users")
def create_user(name: str):
    return {"message": f"User {name} created"}

# PUT Route
@app.put("/users/{user_id}")
def update_user(user_id: int, name: str):
    return {
        "message": f"User {user_id} updated",
        "new_name": name
    }

# DELETE Route
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    return {"message": f"User {user_id} deleted"}