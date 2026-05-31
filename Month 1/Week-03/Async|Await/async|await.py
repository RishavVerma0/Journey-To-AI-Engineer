import asyncio

async def get_prod(prod_id: int) -> dict:
    """Simulates fetching the product details"""
    await asyncio.sleep(1)
    return {
        "id": prod_id,
        "name": "Wireless Mouse",
        "category": "Electronics"
    }

async def get_inventory(prod_id: int) -> dict:
    """Simulates checking inventory."""
    await asyncio.sleep(2)
    return {
        "product_id": prod_id,
        "stock": 42
    }

async def get_price(prod_id: int) -> dict:
    """Simulates fetching pricing information."""
    await asyncio.sleep(1.5)
    return {
        "product_id": prod_id,
        "price": 29.99,
        "Currency": "USD"
    }

async def get_prod_details(prod_id: int) -> dict:
     """
    Fetch product information, inventory,
    and pricing concurrently.
    """
     product, inventory, price = await asyncio.gather(
         get_prod(prod_id),
         get_inventory(prod_id),
         get_price(prod_id)
     )

     return {
         **product,
         **inventory,
         **price
     }


async def main():
    product = await get_prod_details(101)

    print("Product Details.")

    for key, value in product.items():
          print(f"{key}: {value}")

if __name__ == "__main__":

    asyncio.run(main())