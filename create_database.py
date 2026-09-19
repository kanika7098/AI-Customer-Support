import sqlite3
from pathlib import Path


# --------------------------------------------------
# 1. Create database folder
# --------------------------------------------------

Path("data/database").mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# 2. Connect to SQLite database
# --------------------------------------------------

connection = sqlite3.connect(
    "data/database/orders.db"
)

cursor = connection.cursor()


# --------------------------------------------------
# 3. Create orders table
# --------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (

    order_id TEXT PRIMARY KEY,

    customer_name TEXT NOT NULL,

    product_name TEXT NOT NULL,

    order_status TEXT NOT NULL,

    order_date TEXT NOT NULL,

    expected_delivery TEXT NOT NULL,

    tracking_number TEXT

)
""")


# --------------------------------------------------
# 4. Sample orders
# --------------------------------------------------

orders = [

    (
        "ORD1001",
        "Amit Sharma",
        "Wireless Headphones",
        "Shipped",
        "2026-09-15",
        "2026-09-22",
        "TRK1001001"
    ),

    (
        "ORD1002",
        "Priya Patel",
        "Laptop Backpack",
        "Processing",
        "2026-09-18",
        "2026-09-24",
        None
    ),

    (
        "ORD1003",
        "Rahul Verma",
        "Mechanical Keyboard",
        "Delivered",
        "2026-09-10",
        "2026-09-15",
        "TRK1003003"
    ),

    (
        "ORD1004",
        "Sneha Joshi",
        "Smart Watch",
        "Shipped",
        "2026-09-16",
        "2026-09-23",
        "TRK1004004"
    ),

    (
        "ORD1005",
        "Vikram Singh",
        "USB-C Hub",
        "Cancelled",
        "2026-09-12",
        "2026-09-18",
        None
    )

]


# --------------------------------------------------
# 5. Insert sample orders
# --------------------------------------------------

cursor.executemany("""
INSERT OR REPLACE INTO orders (
    order_id,
    customer_name,
    product_name,
    order_status,
    order_date,
    expected_delivery,
    tracking_number
)

VALUES (?, ?, ?, ?, ?, ?, ?)
""", orders)


# --------------------------------------------------
# 6. Save changes
# --------------------------------------------------

connection.commit()


# --------------------------------------------------
# 7. Display database information
# --------------------------------------------------

cursor.execute(
    "SELECT * FROM orders"
)

all_orders = cursor.fetchall()


print("\n" + "=" * 70)
print("ORDER DATABASE CREATED")
print("=" * 70)

print(f"\nTotal orders: {len(all_orders)}")

for order in all_orders:

    print("\nOrder ID:", order[0])
    print("Customer:", order[1])
    print("Product:", order[2])
    print("Status:", order[3])
    print("Order Date:", order[4])
    print("Expected Delivery:", order[5])
    print("Tracking Number:", order[6])


# --------------------------------------------------
# 8. Close database
# --------------------------------------------------

connection.close()


print("\n" + "=" * 70)
print("Database saved successfully!")
print("=" * 70)