# database.py

# Initialize the in-memory database
db: dict = {}

# Seed the database immediately on module import
db.update({
    str(i): {
        "id": str(i),
        "name": f"Item {i}",
        "description": f"Description for Item {i}",
        "price": 100.0 + i,
        "in_stock": True
    }
    for i in range(1, 201)
})

print(f"📦 Database initialized and seeded with {len(db)} items.")