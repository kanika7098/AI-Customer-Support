import sqlite3
from datetime import datetime

DATABASE_PATH = "data/database/orders.db"


def create_ticket(
    issue,
    customer_name="Unknown",
    order_id=None,
    priority="Medium"
):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO support_tickets
        (
            customer_name,
            order_id,
            issue,
            priority,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        customer_name,
        order_id,
        issue,
        priority,
        "Open",
        created_at
    ))

    ticket_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return ticket_id