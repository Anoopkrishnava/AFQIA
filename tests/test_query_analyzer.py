from analyzer.query_analyzer import (
    analyze_query,
    check_query_impact,
    get_impact_level,
    get_execution_risk,
    analyze_query_impact
)

def test_select_query():
    query = "SELECT sender, message FROM messages;"

    result = analyze_query(query)

    assert result["tables"] == ["messages"]
    assert "sender" in result["columns"]
    assert "message" in result["columns"]


def test_where_clause():
    query = """
    SELECT message
    FROM messages
    WHERE sender = 'Alice';
    """

    result = analyze_query(query)

    assert "message" in result["columns"]
    assert "sender" in result["columns"]


def test_removed_column_impact():
    query = "SELECT message FROM messages;"

    changes = [
        {
            "type": "removed_column",
            "table": "messages",
            "column": "message"
        },
        {
            "type": "added_column",
            "table": "messages",
            "column": "timestamp"
        }
    ]

    result = check_query_impact(query, changes)

    assert {
        "type": "removed_column",
        "table": "messages",
        "column": "message"
    } in result


def test_changed_column_type_impact():
    query = "SELECT sender FROM messages;"

    changes = [
        {
            "type": "changed_column_type",
            "table": "messages",
            "column": "sender",
            "old_type": "TEXT",
            "new_type": "INTEGER"
        }
    ]

    result = check_query_impact(query, changes)

    assert {
        "type": "changed_column_type",
        "table": "messages",
        "column": "sender",
        "old_type": "TEXT",
        "new_type": "INTEGER"
    } in result


def test_table_alias():
    query = """
    SELECT m.sender, m.message
    FROM messages AS m;
    """

    result = analyze_query(query)

    assert result["tables"] == ["messages"]
    assert "sender" in result["columns"]
    assert "message" in result["columns"]


def test_high_impact_removed_column():
    query = "SELECT message FROM messages;"

    changes = [
        {
            "type": "removed_column",
            "table": "messages",
            "column": "message"
        }
    ]

    result = get_impact_level(query, changes)

    assert result == "HIGH"


def test_high_impact_changed_type():
    query = "SELECT sender FROM messages;"

    changes = [
        {
            "type": "changed_column_type",
            "table": "messages",
            "column": "sender",
            "old_type": "TEXT",
            "new_type": "INTEGER"
        }
    ]

    result = get_impact_level(query, changes)

    assert result == "HIGH"


def test_no_impact_unrelated_change():
    query = "SELECT sender, message FROM messages;"

    changes = [
        {
            "type": "added_column",
            "table": "messages",
            "column": "timestamp"
        }
    ]

    result = get_impact_level(query, changes)

    assert result == "NONE"
    
def test_breaking_removed_column():
    query = "SELECT message FROM messages;"

    changes = [
        {
            "type": "removed_column",
            "table": "messages",
            "column": "message"
        }
    ]

    result = get_execution_risk(query, changes)

    assert result == "BREAKING"


def test_affected_changed_type():
    query = "SELECT message FROM messages;"

    changes = [
        {
            "type": "changed_column_type",
            "table": "messages",
            "column": "message",
            "old_type": "TEXT",
            "new_type": "INTEGER"
        }
    ]

    result = get_execution_risk(query, changes)

    assert result == "AFFECTED"


def test_no_execution_risk():
    query = "SELECT sender, message FROM messages;"

    changes = [
        {
            "type": "added_column",
            "table": "messages",
            "column": "timestamp"
        }
    ]

    result = get_execution_risk(query, changes)

    assert result == "NONE"
    
def test_complete_query_impact_analysis():
    query = """
    SELECT sender, message
    FROM messages;
    """

    changes = [
        {
            "type": "removed_column",
            "table": "messages",
            "column": "message"
        },
        {
            "type": "added_column",
            "table": "messages",
            "column": "timestamp"
        }
    ]

    result = analyze_query_impact(query, changes)

    assert result["tables"] == ["messages"]
    assert "sender" in result["columns"]
    assert "message" in result["columns"]

    assert {
        "type": "removed_column",
        "table": "messages",
        "column": "message"
    } in result["impacted_changes"]

    assert result["impact_level"] == "HIGH"
    assert result["execution_risk"] == "BREAKING"
    
def test_query_with_where_condition():
    query = """
    SELECT sender, message
    FROM messages
    WHERE sender = 'Alice';
    """

    result = analyze_query(query)

    assert result["tables"] == ["messages"]
    assert "sender" in result["columns"]
    assert "message" in result["columns"]
    
def test_query_with_table_alias():
    query = """
    SELECT m.sender, m.message
    FROM messages AS m;
    """

    result = analyze_query(query)

    assert result["tables"] == ["messages"]
    assert "sender" in result["columns"]
    assert "message" in result["columns"]
    
def test_query_affected_by_removed_table():
    query = """
    SELECT sender, message
    FROM messages;
    """

    changes = [
        {
            "type": "removed_table",
            "table": "messages"
        }
    ]

    result = analyze_query_impact(query, changes)

    assert result["impact_level"] == "HIGH"
    assert result["execution_risk"] == "BREAKING"
    
def test_query_unaffected_by_unrelated_change():
    query = """
    SELECT sender, message
    FROM messages;
    """

    changes = [
        {
            "type": "added_column",
            "table": "messages",
            "column": "timestamp"
        }
    ]

    result = analyze_query_impact(query, changes)

    assert result["impacted_changes"] == []
    assert result["impact_level"] == "NONE"
    assert result["execution_risk"] == "NONE"
    
def test_query_affected_by_changed_column_type():
    query = """
    SELECT sender, message
    FROM messages;
    """

    changes = [
        {
            "type": "changed_column_type",
            "table": "messages",
            "column": "message",
            "old_type": "TEXT",
            "new_type": "INTEGER"
        }
    ]

    result = analyze_query_impact(query, changes)

    assert result["impact_level"] == "HIGH"
    assert result["execution_risk"] == "AFFECTED"
    
def test_query_with_join():
    query = """
    SELECT m.message, u.name
    FROM messages AS m
    JOIN users AS u ON m.sender_id = u.id;
    """

    result = analyze_query(query)

    assert result["tables"] == ["messages", "users"]
    assert "message" in result["columns"]
    assert "name" in result["columns"]
    
def test_join_query_affected_by_removed_table():
    query = """
    SELECT m.message, u.name
    FROM messages AS m
    JOIN users AS u ON m.sender_id = u.id;
    """

    changes = [
        {
            "type": "removed_table",
            "table": "users"
        }
    ]

    result = analyze_query_impact(query, changes)

    assert result["tables"] == ["messages", "users"]
    assert result["impact_level"] == "HIGH"
    assert result["execution_risk"] == "BREAKING"
    
def test_join_query_affected_by_removed_join_column():
    query = """
    SELECT m.message, u.name
    FROM messages AS m
    JOIN users AS u ON m.sender_id = u.id;
    """

    changes = [
        {
            "type": "removed_column",
            "table": "messages",
            "column": "sender_id"
        }
    ]

    result = analyze_query_impact(query, changes)

    assert result["impact_level"] == "HIGH"
    assert result["execution_risk"] == "BREAKING"
    
def test_join_query_affected_by_removed_right_join_column():
    query = """
    SELECT m.message, u.name
    FROM messages AS m
    JOIN users AS u ON m.sender_id = u.id;
    """

    changes = [
        {
            "type": "removed_column",
            "table": "users",
            "column": "id"
        }
    ]

    result = analyze_query_impact(query, changes)

    assert result["impact_level"] == "HIGH"
    assert result["execution_risk"] == "BREAKING"
    
def test_join_query_unaffected_by_unrelated_column():
    query = """
    SELECT m.message, u.name
    FROM messages AS m
    JOIN users AS u ON m.sender_id = u.id;
    """

    changes = [
        {
            "type": "added_column",
            "table": "users",
            "column": "email"
        }
    ]

    result = analyze_query_impact(query, changes)

    assert result["impacted_changes"] == []
    assert result["impact_level"] == "NONE"
    assert result["execution_risk"] == "NONE"
    
def test_query_with_multiple_schema_changes():
    query = """
    SELECT sender, message
    FROM messages;
    """

    changes = [
        {
            "type": "removed_column",
            "table": "messages",
            "column": "message"
        },
        {
            "type": "changed_column_type",
            "table": "messages",
            "column": "sender",
            "old_type": "TEXT",
            "new_type": "INTEGER"
        },
        {
            "type": "added_column",
            "table": "messages",
            "column": "timestamp"
        }
    ]

    result = analyze_query_impact(query, changes)

    assert len(result["impacted_changes"]) == 2
    assert result["impact_level"] == "HIGH"
    assert result["execution_risk"] == "BREAKING"
    

