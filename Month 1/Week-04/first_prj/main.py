from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI(title="My CRUD API", version="1.0.0")

# ----- Schema -----
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None

# ----- In-memory DB -----
db: dict = {}

# ----- Endpoints -----
@app.get("/")
def root():
    return {"message": "Welcome to my CRUD API 🚀"}

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
    db[item_id] = {"id": item_id, **item.dict()}
    return {"message": "Created", "item": db[item_id]}

@app.put("/items/{item_id}")
def update_item(item_id: str, update: ItemUpdate):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in update.dict(exclude_unset=True).items():
        db[item_id][field] = value
    return {"message": "Updated", "item": db[item_id]}

@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted = db.pop(item_id)
    return {"message": "Deleted", "item": deleted}