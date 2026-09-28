from analyzer.impact_analyzer import analyze_database_query


def test_analyze_database_query():
    result = analyze_database_query(
        "test_data/database_v1.db",
        "test_data/database_v2_removed_column.db",
        "SELECT sender, message FROM messages;"
    )

    assert result["tables"] == ["messages"]
    assert "sender" in result["columns"]
    assert "message" in result["columns"]

    assert len(result["impacted_changes"]) == 1
    assert result["affected"] is True

def test_added_column_does_not_break_query():
    result = analyze_database_query(
        "test_data/database_v1.db",
        "test_data/database_v2.db",
        "SELECT sender, message FROM messages;"
    )

    assert result["tables"] == ["messages"]
    assert "sender" in result["columns"]
    assert "message" in result["columns"]

    
    assert result["affected"] is False

def test_changed_column_type_impacts_query():
    result = analyze_database_query(
        "test_data/database_v1.db",
        "test_data/database_v2_changed_type.db",
        "SELECT sender, message FROM messages;"
    )

    assert result["tables"] == ["messages"]
    assert "sender" in result["columns"]

    assert len(result["impacted_changes"]) == 1
    assert result["affected"] is True

def test_removed_table_impacts_query():
    result = analyze_database_query(
        "test_data/database_v1_with_users.db",
        "test_data/database_v2_removed_table.db",
        "SELECT name FROM users;"
    )

    assert result["tables"] == ["users"]
    assert "name" in result["columns"]

    assert len(result["impacted_changes"]) == 1
    assert result["affected"] is True