import sqlite3

connection = sqlite3.connect("test_data/database_v2.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    sender TEXT,
    message TEXT,
    timestamp INTEGER
)
""")

connection.commit()
connection.close()

print("Database V2 created successfully.")
