import sqlite3

connection = sqlite3.connect("test_data/database_v1.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    sender TEXT,
    message TEXT
)
""")

connection.commit()
connection.close()

print("Database V1 created successfully.")
