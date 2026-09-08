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

    assert {
        "type": "added_column",
        "table": "messages",
        "column": "timestamp"
    } in changes


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

    assert {
        "type": "removed_column",
        "table": "messages",
        "column": "message"
    } in changes


def test_added_table():
    schema_v1 = {
        "messages": {
            "id": "INTEGER"
        }
    }

    schema_v2 = {
        "messages": {
            "id": "INTEGER"
        },
        "users": {
            "id": "INTEGER"
        }
    }

    changes = compare_schemas(schema_v1, schema_v2)

    assert {
        "type": "added_table",
        "table": "users"
    } in changes


def test_removed_table():
    schema_v1 = {
        "messages": {
            "id": "INTEGER"
        },
        "users": {
            "id": "INTEGER"
        }
    }

    schema_v2 = {
        "messages": {
            "id": "INTEGER"
        }
    }

    changes = compare_schemas(schema_v1, schema_v2)

    assert {
        "type": "removed_table",
        "table": "users"
    } in changes


def test_changed_column_type():
    schema_v1 = {
        "messages": {
            "id": "INTEGER",
            "message": "TEXT"
        }
    }

    schema_v2 = {
        "messages": {
            "id": "INTEGER",
            "message": "INTEGER"
        }
    }

    changes = compare_schemas(schema_v1, schema_v2)

    assert {
        "type": "changed_column_type",
        "table": "messages",
        "column": "message",
        "old_type": "TEXT",
        "new_type": "INTEGER"
    } in changes
