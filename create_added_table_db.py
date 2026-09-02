import sqlite3

connection = sqlite3.connect(
    "test_data/database_v2_added_table.db"
)

cursor = connection.cursor()

# Existing table
cursor.execute("""
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    sender TEXT,
    message TEXT
)
""")

# New table
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

connection.commit()
connection.close()

print("Test database created successfully.")
