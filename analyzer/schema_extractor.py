import sqlite3


def extract_schema(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    schema = {}

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
    """)

    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]

        cursor.execute(f"PRAGMA table_info('{table_name}')")
        columns = cursor.fetchall()

        schema[table_name] = {}

        for column in columns:
            column_name = column[1]
            data_type = column[2]

            schema[table_name][column_name] = data_type

    connection.close()

    return schema
