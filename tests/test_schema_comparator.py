from analyzer.schema_comparator import compare_schemas


def test_added_column():
    schema_v1 = {
        "messages": {
            "id": "INTEGER",
            "sender": "TEXT",
            "message": "TEXT"
        }
    }

    schema_v2 = {
        "messages": {
            "id": "INTEGER",
            "sender": "TEXT",
            "message": "TEXT",
            "timestamp": "INTEGER"
        }
    }

    changes = compare_schemas(schema_v1, schema_v2)

    assert "Added column: messages.timestamp" in changes
    
def test_removed_column():
    schema_v1 = {
        "messages": {
            "id": "INTEGER",
            "sender": "TEXT",
            "message": "TEXT"
        }
    }

    schema_v2 = {
        "messages": {
            "id": "INTEGER",
            "sender": "TEXT"
        }
    }

    changes = compare_schemas(schema_v1, schema_v2)

    assert "Removed column: messages.message" in changes
    
def test_added_table():
    schema_v1 = {
        "messages": {
            "id": "INTEGER",
            "sender": "TEXT",
            "message": "TEXT"
        }
    }

    schema_v2 = {
        "messages": {
            "id": "INTEGER",
            "sender": "TEXT",
            "message": "TEXT"
        },
        "users": {
            "id": "INTEGER",
            "name": "TEXT"
        }
    }

    changes = compare_schemas(schema_v1, schema_v2)

    assert "Added table: users" in changes
    
def test_removed_table():
    schema_v1 = {
        "messages": {
            "id": "INTEGER",
            "sender": "TEXT",
            "message": "TEXT"
        },
        "users": {
            "id": "INTEGER",
            "name": "TEXT"
        }
    }

    schema_v2 = {
        "messages": {
            "id": "INTEGER",
            "sender": "TEXT",
            "message": "TEXT"
        }
    }

    changes = compare_schemas(schema_v1, schema_v2)

    assert "Removed table: users" in changes
    
def test_changed_column_type():
    schema_v1 = {
        "messages": {
            "id": "INTEGER",
            "sender": "TEXT",
            "message": "TEXT"
        }
    }

    schema_v2 = {
        "messages": {
            "id": "INTEGER",
            "sender": "TEXT",
            "message": "INTEGER"
        }
    }

    changes = compare_schemas(schema_v1, schema_v2)

    assert "Changed column type: messages.message (TEXT → INTEGER)" in changes
