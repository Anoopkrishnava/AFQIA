import sqlite3
import os

db_path = "test_data/database_v2_removed_table.db"

# Recreate the test database from scratch
if os.path.exists(db_path):
    os.remove(db_path)

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Keep messages in V2, but remove users
cursor.execute("""
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    sender TEXT,
    message TEXT
)
""")

connection.commit()
connection.close()

print("Test database created successfully.")