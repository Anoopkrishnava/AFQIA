import sqlite3

# Old Database — Version 1
conn = sqlite3.connect("old_database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE messages (
    id INTEGER,
    sender TEXT,
    message TEXT
)
""")

conn.commit()
conn.close()


# New Database — Version 2
conn = sqlite3.connect("new_database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE messages (
    id INTEGER,
    sender TEXT,
    content TEXT,
    timestamp TEXT
)
""")

conn.commit()
conn.close()

print("Demo databases created successfully.")
