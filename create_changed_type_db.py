import sqlite3

connection = sqlite3.connect(
    "test_data/database_v2_changed_type.db"
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    sender TEXT,
    message INTEGER
)
""")

connection.commit()
connection.close()

print("Changed-type test database created successfully.")
