import sqlite3

connection = sqlite3.connect(
    "test_data/database_v2_removed_column.db"
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    sender TEXT
)
""")

connection.commit()
connection.close()

print("Test database created successfully.")
