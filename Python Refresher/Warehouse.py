from datetime import datetime
from enum import Enum


# ---------------------------------------------------------
# ENUMS
# ---------------------------------------------------------

class OrderStatus(Enum):
    CREATED = "Created"
    CONFIRMED = "Confirmed"
    PACKED = "Packed"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class ShipmentStatus(Enum):
    CREATED = "Created"
    PICKED_UP = "Picked Up"
    IN_TRANSIT = "In Transit"
    OUT_FOR_DELIVERY = "Out For Delivery"
    DELIVERED = "Delivered"


# ---------------------------------------------------------
# PRODUCT
# ---------------------------------------------------------

class Product:

    def __init__(self, product_id, name, price, category):

        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category

    def __str__(self):

        return (
            f"{self.product_id} | "
            f"{self.name} | "
            f"₹{self.price}"
        )


# ---------------------------------------------------------
# INVENTORY ITEM
# ---------------------------------------------------------

class InventoryItem:

    def __init__(self, product, quantity):

        self.product = product
        self.quantity = quantity
        self.reserved = 0

    @property
    def available_quantity(self):

        return self.quantity - self.reserved

    def reserve(self, amount):

        if amount <= 0:

            raise ValueError(
                "Quantity must be greater than zero."
            )

        if amount > self.available_quantity:

            raise ValueError(
                f"Not enough stock for {self.product.name}"
            )

        self.reserved += amount

    def release(self, amount):

        if amount > self.reserved:

            raise ValueError(
                "Cannot release more than reserved quantity."
            )

        self.reserved -= amount

    def consume_reserved(self, amount):

        if amount > self.reserved:

            raise ValueError(
                "Invalid reserved quantity."
            )

        self.quantity -= amount
        self.reserved -= amount


# ---------------------------------------------------------
# WAREHOUSE
# ---------------------------------------------------------

class Warehouse:

    def __init__(self, warehouse_id, location):

        self.warehouse_id = warehouse_id
        self.location = location

        self.inventory = {}

    # -----------------------------------------------------
    # ADD PRODUCT
    # -----------------------------------------------------

    def add_product(self, product, quantity):

        if product.product_id in self.inventory:

            self.inventory[
                product.product_id
            ].quantity += quantity

        else:

            self.inventory[
                product.product_id
            ] = InventoryItem(
                product,
                quantity
            )

    # -----------------------------------------------------
    # CHECK STOCK
    # -----------------------------------------------------

    def get_item(self, product_id):

        if product_id not in self.inventory:

            raise ValueError(
                f"Product {product_id} not found."
            )

        return self.inventory[product_id]

    # -----------------------------------------------------
    # RESERVE STOCK
    # -----------------------------------------------------

    def reserve_stock(self, product_id, quantity):

        item = self.get_item(product_id)

        item.reserve(quantity)

    # -----------------------------------------------------
    # CONSUME STOCK
    # -----------------------------------------------------

    def consume_stock(self, product_id, quantity):

        item = self.get_item(product_id)

        item.consume_reserved(quantity)

    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------

    def display_inventory(self):

        print("\n" + "=" * 60)

        print(
            f"Warehouse: {self.warehouse_id} "
            f"({self.location})"
        )

        for item in self.inventory.values():

            print(
                f"{item.product.name:20} "
                f"Total: {item.quantity:4} "
                f"Reserved: {item.reserved:4} "
                f"Available: {item.available_quantity:4}"
            )

        print("=" * 60)


# ---------------------------------------------------------
# ORDER ITEM
# ---------------------------------------------------------

class OrderItem:

    def __init__(self, product, quantity):

        self.product = product
        self.quantity = quantity

    @property
    def total_price(self):

        return self.product.price * self.quantity


# ---------------------------------------------------------
# CUSTOMER
# ---------------------------------------------------------

class Customer:

    def __init__(self, customer_id, name, address):

        self.customer_id = customer_id
        self.name = name
        self.address = address

        self.orders = []

    def add_order(self, order):

        self.orders.append(order)


# ---------------------------------------------------------
# SHIPMENT
# ---------------------------------------------------------

class Shipment:

    counter = 5000

    def __init__(self, order, warehouse):

        Shipment.counter += 1

        self.shipment_id = f"SHP{Shipment.counter}"

        self.order = order
        self.warehouse = warehouse

        self.status = ShipmentStatus.CREATED

        self.history = []

        self.created_at = datetime.now()

        self.add_history(
            "Shipment created"
        )

    def add_history(self, message):

        self.history.append({
            "time": datetime.now(),
            "message": message
        })

    def update_status(self, status):

        self.status = status

        self.add_history(
            f"Status changed to {status.value}"
        )

    def display_tracking(self):

        print("\nSHIPMENT TRACKING")

        print(
            f"Shipment ID : {self.shipment_id}"
        )

        print(
            f"Order ID    : {self.order.order_id}"
        )

        print(
            f"Status      : {self.status.value}"
        )

        print("\nHistory:")

        for event in self.history:

            print(
                event["time"].strftime("%H:%M:%S"),
                "-",
                event["message"]
            )


# ---------------------------------------------------------
# ORDER
# ---------------------------------------------------------

class Order:

    counter = 10000

    def __init__(self, customer):

        Order.counter += 1

        self.order_id = f"ORD{Order.counter}"

        self.customer = customer

        self.items = []

        self.status = OrderStatus.CREATED

        self.shipment = None

        self.created_at = datetime.now()

    # -----------------------------------------------------
    # ADD ITEM
    # -----------------------------------------------------

    def add_item(self, product, quantity):

        if quantity <= 0:

            raise ValueError(
                "Quantity must be positive."
            )

        self.items.append(
            OrderItem(
                product,
                quantity
            )
        )

    # -----------------------------------------------------
    # TOTAL
    # -----------------------------------------------------

    @property
    def total_amount(self):

        return sum(
            item.total_price
            for item in self.items
        )

    # -----------------------------------------------------
    # CONFIRM
    # -----------------------------------------------------

    def confirm(self, warehouse):

        if not self.items:

            raise ValueError(
                "Cannot confirm empty order."
            )

        # First reserve everything.
        # If one item fails, the order should not
        # partially reserve stock.

        reserved_items = []

        try:

            for item in self.items:

                warehouse.reserve_stock(
                    item.product.product_id,
                    item.quantity
                )

                reserved_items.append(item)

            self.status = OrderStatus.CONFIRMED

        except Exception as error:

            # Roll back previously reserved stock

            for item in reserved_items:

                inventory_item = warehouse.get_item(
                    item.product.product_id
                )

                inventory_item.release(
                    item.quantity
                )

            raise error

    # -----------------------------------------------------
    # PACK
    # -----------------------------------------------------

    def pack(self, warehouse):

        if self.status != OrderStatus.CONFIRMED:

            raise Exception(
                "Order must be confirmed first."
            )

        for item in self.items:

            warehouse.consume_stock(
                item.product.product_id,
                item.quantity
            )

        self.status = OrderStatus.PACKED

    # -----------------------------------------------------
    # SHIP
    # -----------------------------------------------------

    def ship(self, warehouse):

        if self.status != OrderStatus.PACKED:

            raise Exception(
                "Order must be packed first."
            )

        self.shipment = Shipment(
            self,
            warehouse
        )

        self.shipment.update_status(
            ShipmentStatus.PICKED_UP
        )

        self.status = OrderStatus.SHIPPED

    # -----------------------------------------------------
    # DELIVER
    # -----------------------------------------------------

    def deliver(self):

        if self.status != OrderStatus.SHIPPED:

            raise Exception(
                "Order must be shipped first."
            )

        assert self.shipment is not None
        self.shipment.update_status(
            ShipmentStatus.IN_TRANSIT
        )

        self.shipment.update_status(
            ShipmentStatus.OUT_FOR_DELIVERY
        )

        self.shipment.update_status(
            ShipmentStatus.DELIVERED
        )

        self.status = OrderStatus.DELIVERED

    # -----------------------------------------------------
    # DISPLAY
    # -----------------------------------------------------

    def display(self):

        print("\n" + "=" * 60)

        print(f"Order ID : {self.order_id}")
        print(f"Customer : {self.customer.name}")
        print(f"Status   : {self.status.value}")

        print("\nItems:")

        for item in self.items:

            print(
                f"{item.product.name:20} "
                f"x {item.quantity:3} "
                f"₹{item.total_price}"
            )

        print(
            f"\nTOTAL: ₹{self.total_amount}"
        )

        print("=" * 60)


# ---------------------------------------------------------
# ORDER MANAGEMENT SYSTEM
# ---------------------------------------------------------

class OrderManagementSystem:

    def __init__(self):

        self.customers = {}
        self.products = {}
        self.warehouses = {}
        self.orders = {}

    # -----------------------------------------------------
    # REGISTER
    # -----------------------------------------------------

    def add_customer(self, customer):

        self.customers[
            customer.customer_id
        ] = customer

    def add_product(self, product):

        self.products[
            product.product_id
        ] = product

    def add_warehouse(self, warehouse):

        self.warehouses[
            warehouse.warehouse_id
        ] = warehouse

    # -----------------------------------------------------
    # CREATE ORDER
    # -----------------------------------------------------

    def create_order(self, customer_id):

        if customer_id not in self.customers:

            raise ValueError(
                "Customer not found."
            )

        customer = self.customers[customer_id]

        order = Order(customer)

        customer.add_order(order)

        self.orders[order.order_id] = order

        return order

    # -----------------------------------------------------
    # FIND WAREHOUSE WITH STOCK
    # -----------------------------------------------------

    def find_warehouse(self, order):

        for warehouse in self.warehouses.values():

            can_fulfill = True

            for item in order.items:

                inventory = warehouse.get_item(
                    item.product.product_id
                )

                if (
                    inventory.available_quantity
                    < item.quantity
                ):
                    can_fulfill = False
                    break

            if can_fulfill:

                return warehouse

        return None


# ---------------------------------------------------------
# DEMO
# ---------------------------------------------------------

system = OrderManagementSystem()


# ---------------------------------------------------------
# PRODUCTS
# ---------------------------------------------------------

laptop = Product(
    "P101",
    "Laptop",
    65000,
    "Electronics"
)

mouse = Product(
    "P102",
    "Wireless Mouse",
    1200,
    "Electronics"
)

keyboard = Product(
    "P103",
    "Mechanical Keyboard",
    4500,
    "Electronics"
)


system.add_product(laptop)
system.add_product(mouse)
system.add_product(keyboard)


# ---------------------------------------------------------
# WAREHOUSES
# ---------------------------------------------------------

warehouse_delhi = Warehouse(
    "WH01",
    "Delhi"
)

warehouse_gurgaon = Warehouse(
    "WH02",
    "Gurgaon"
)


warehouse_delhi.add_product(laptop, 10)
warehouse_delhi.add_product(mouse, 50)
warehouse_delhi.add_product(keyboard, 20)


warehouse_gurgaon.add_product(laptop, 5)
warehouse_gurgaon.add_product(mouse, 30)
warehouse_gurgaon.add_product(keyboard, 10)


system.add_warehouse(warehouse_delhi)
system.add_warehouse(warehouse_gurgaon)


# ---------------------------------------------------------
# CUSTOMER
# ---------------------------------------------------------

customer = Customer(
    "C101",
    "Rishav",
    "Gurgaon"
)

system.add_customer(customer)


# ---------------------------------------------------------
# CREATE ORDER
# ---------------------------------------------------------

order = system.create_order("C101")


order.add_item(
    laptop,
    2
)

order.add_item(
    mouse,
    3
)

order.add_item(
    keyboard,
    1
)


# ---------------------------------------------------------
# FIND FULFILLING WAREHOUSE
# ---------------------------------------------------------

warehouse = system.find_warehouse(order)


if warehouse:

    print(
        f"Order can be fulfilled from "
        f"{warehouse.location}"
    )

    # Reserve inventory

    order.confirm(warehouse)

    # Pack order

    order.pack(warehouse)

    # Ship order

    order.ship(warehouse)

    # Display

    order.display()

    warehouse.display_inventory()

    # Deliver

    order.deliver()

    order.display()

    assert order.shipment is not None
    order.shipment.display_tracking()

else:

    print(
        "No warehouse has sufficient inventory."
    )