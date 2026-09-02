import sqlite3

connection = sqlite3.connect(
    "test_data/database_v1_with_users.db"
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

# Table that will be removed in V2
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

connection.commit()
connection.close()

print("V1 test database created successfully.")
