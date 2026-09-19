import sqlite3
from pathlib import Path


# --------------------------------------------------
# 1. Database location
# --------------------------------------------------

DATABASE_PATH = "data/database/orders.db"


# --------------------------------------------------
# 2. Make sure database folder exists
# --------------------------------------------------

Path("data/database").mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# 3. Connect to database
# --------------------------------------------------

connection = sqlite3.connect(
    DATABASE_PATH
)

cursor = connection.cursor()


# --------------------------------------------------
# 4. Create support tickets table
# --------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS support_tickets (

    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_name TEXT,

    order_id TEXT,

    issue TEXT NOT NULL,

    priority TEXT NOT NULL,

    status TEXT NOT NULL,

    created_at TEXT NOT NULL

)
""")


# --------------------------------------------------
# 5. Save changes
# --------------------------------------------------

connection.commit()


# --------------------------------------------------
# 6. Check table
# --------------------------------------------------

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'table'
AND name = 'support_tickets'
""")

table = cursor.fetchone()


# --------------------------------------------------
# 7. Display result
# --------------------------------------------------

print("\n" + "=" * 60)

if table:

    print("SUPPORT TICKET SYSTEM CREATED")
    print("=" * 60)

    print("\nTable name:")
    print("support_tickets")

    print("\nColumns:")

    print("- ticket_id")
    print("- customer_name")
    print("- order_id")
    print("- issue")
    print("- priority")
    print("- status")
    print("- created_at")

else:

    print("Could not create support ticket table.")

print("=" * 60)


# --------------------------------------------------
# 8. Close database
# --------------------------------------------------

connection.close()