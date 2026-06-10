# main.py
import uuid
from fastapi import FastAPI, HTTPException

# Import the shared database instance and schemas
from database import db
from models import Item, ItemUpdate

app = FastAPI(title="My CRUD API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Welcome to my CRUD API 🚀"}

@app.get("/debug")
def debug_db():
    # This will now correctly show 200 items because it references the shared 'db'
    keys = list(db.keys())
    return {
        "count": len(db),
        "first_5_keys": keys[:5]
    }

@app.get("/items")
def get_all_items():
    return {"items": list(db.values()), "count": len(db)}

@app.get("/items/{item_id}")
def get_item(item_id: str):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]

@app.post("/items", status_code=201)
def create_item(item: Item):
    item_id = str(uuid.uuid4())[:8]
    db[item_id] = {"id": item_id, **item.model_dump()}
    return {"message": "Created", "item": db[item_id]}

@app.put("/items/{item_id}")
def update_item(item_id: str, update: ItemUpdate):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    update_data = update.model_dump(exclude_unset=True)
    db[item_id].update(update_data)
    return {"message": "Updated", "item": db[item_id]}

@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted = db.pop(item_id)
    return {"message": "Deleted", "item": deleted}