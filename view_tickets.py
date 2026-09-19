import sqlite3

DATABASE_PATH = "data/database/orders.db"


def view_tickets():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            ticket_id,
            customer_name,
            order_id,
            issue,
            priority,
            status,
            created_at
        FROM support_tickets
        ORDER BY ticket_id DESC
    """)

    tickets = cursor.fetchall()

    connection.close()

    print("\n" + "=" * 70)
    print("SUPPORT TICKETS")
    print("=" * 70)

    if not tickets:
        print("\nNo support tickets found.")
        return

    for ticket in tickets:
        ticket_id, customer_name, order_id, issue, priority, status, created_at = ticket

        print(f"\nTicket #{ticket_id}")
        print(f"Customer: {customer_name}")
        print(f"Order ID: {order_id if order_id else 'None'}")
        print(f"Priority: {priority}")
        print(f"Status: {status}")
        print(f"Issue: {issue}")
        print(f"Created: {created_at}")
        print("-" * 70)


if __name__ == "__main__":
    view_tickets()