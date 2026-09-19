import sqlite3


# --------------------------------------------------
# Database connection
# --------------------------------------------------

DATABASE_PATH = "data/database/orders.db"


# --------------------------------------------------
# Function to find an order
# --------------------------------------------------

def get_order(order_id):

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            order_id,
            customer_name,
            product_name,
            order_status,
            order_date,
            expected_delivery,
            tracking_number
        FROM orders
        WHERE order_id = ?
    """, (order_id,))

    order = cursor.fetchone()

    connection.close()

    return order


# --------------------------------------------------
# Test order lookup
# --------------------------------------------------

order_id = input("Enter Order ID: ").strip().upper()

order = get_order(order_id)


# --------------------------------------------------
# Display result
# --------------------------------------------------

print("\n" + "=" * 60)

if order:

    print("ORDER FOUND")
    print("=" * 60)

    print(f"Order ID:          {order[0]}")
    print(f"Customer:          {order[1]}")
    print(f"Product:           {order[2]}")
    print(f"Status:            {order[3]}")
    print(f"Order Date:        {order[4]}")
    print(f"Expected Delivery: {order[5]}")
    print(f"Tracking Number:   {order[6] or 'Not available'}")

else:

    print("ORDER NOT FOUND")
    print("=" * 60)

    print(
        f"No order was found with ID: {order_id}"
    )

print("=" * 60)