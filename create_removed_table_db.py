import sqlite3

connection = sqlite3.connect(
    "test_data/database_v2_removed_table.db"
)

cursor = connection.cursor()

# Only the messages table exists in V2
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
