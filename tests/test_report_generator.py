from analyzer.report_generator import generate_report


def test_generate_report_contains_query_information():

    result = {
        "tables": ["messages"],
        "columns": ["sender", "message"],
        "impacted_changes": [],
        "affected": False,
        "schema_changes": [],
        "impact_reason": "The query is not affected by the detected schema changes.",
        "execution_status": "NO PROBLEM",
        "execution_reason": "The existing query can continue to work with the new schema.",
        "affected_elements": [],
        "analysis_result": "No modification is required for the query."
    }

    report = generate_report(
        result,
        "database_v1.db",
        "database_v2.db",
        "SELECT sender, message FROM messages;"
    )

    assert "database_v1.db" in report
    assert "database_v2.db" in report
    assert "SELECT sender, message FROM messages;" in report


def test_generate_report_for_removed_column():

    result = {
        "tables": ["messages"],
        "columns": ["sender", "message"],
        "impacted_changes": [
            {
                "type": "removed_column",
                "table": "messages",
                "column": "message"
            }
        ],
        "affected": True,
        "schema_changes": [
            {
                "type": "removed_column",
                "table": "messages",
                "column": "message"
            }
        ],
        "impact_reason": (
            "The query uses column 'messages.message', "
            "which was removed from the new database schema."
        ),
        "execution_status": "WILL FAIL",
        "execution_reason": (
            "The column 'messages.message' no longer exists "
            "in the new database schema."
        ),
        "affected_elements": ["messages.message"],
        "analysis_result": "Query modification is required."
    }

    report = generate_report(
        result,
        "database_v1.db",
        "database_v2_removed_column.db",
        "SELECT sender, message FROM messages;"
    )

    assert "Removed Column" in report
    assert "messages.message" in report
    assert "WILL FAIL" in report
    assert "Query modification is required." in report


def test_generate_report_for_changed_column_type():

    result = {
        "tables": ["messages"],
        "columns": ["sender", "message"],
        "impacted_changes": [
            {
                "type": "changed_column_type",
                "table": "messages",
                "column": "message",
                "old_type": "TEXT",
                "new_type": "INTEGER"
            }
        ],
        "affected": True,
        "schema_changes": [
            {
                "type": "changed_column_type",
                "table": "messages",
                "column": "message",
                "old_type": "TEXT",
                "new_type": "INTEGER"
            }
        ],
        "impact_reason": (
            "The query uses column 'messages.message', "
            "whose type changed from TEXT to INTEGER."
        ),
        "execution_status": "REQUIRES REVIEW",
        "execution_reason": (
            "The column 'messages.message' changed from "
            "TEXT to INTEGER."
        ),
        "affected_elements": ["messages.message"],
        "analysis_result": "Further analyst review is required."
    }

    report = generate_report(
        result,
        "database_v1.db",
        "database_v2_changed_type.db",
        "SELECT sender, message FROM messages;"
    )

    assert "Changed Column Type" in report
    assert "TEXT" in report
    assert "INTEGER" in report
    assert "REQUIRES REVIEW" in report
    assert "Further analyst review is required." in report


def test_generate_report_for_removed_table():

    result = {
        "tables": ["messages"],
        "columns": ["sender", "message"],
        "impacted_changes": [
            {
                "type": "removed_table",
                "table": "messages"
            }
        ],
        "affected": True,
        "schema_changes": [
            {
                "type": "removed_table",
                "table": "messages"
            }
        ],
        "impact_reason": (
            "The query uses table 'messages', "
            "which was removed from the new database schema."
        ),
        "execution_status": "WILL FAIL",
        "execution_reason": (
            "The table 'messages' no longer exists "
            "in the new database schema."
        ),
        "affected_elements": ["messages"],
        "analysis_result": "Query modification is required."
    }

    report = generate_report(
        result,
        "database_v1.db",
        "database_v2_removed_table.db",
        "SELECT sender, message FROM messages;"
    )

    assert "Removed Table" in report
    assert "messages" in report
    assert "WILL FAIL" in report
    assert "Query modification is required." in report


def test_generate_report_for_added_column():

    result = {
        "tables": ["messages"],
        "columns": ["sender", "message"],
        "impacted_changes": [],
        "affected": False,
        "schema_changes": [
            {
                "type": "added_column",
                "table": "messages",
                "column": "timestamp"
            }
        ],
        "impact_reason": (
            "The query is not affected by the detected schema changes."
        ),
        "execution_status": "NO PROBLEM",
        "execution_reason": (
            "The existing query can continue to work with the new schema."
        ),
        "affected_elements": [],
        "analysis_result": (
            "No modification is required for the query."
        )
    }

    report = generate_report(
        result,
        "database_v1.db",
        "database_v2.db",
        "SELECT sender, message FROM messages;"
    )

    assert "Added Column" in report
    assert "timestamp" in report
    assert "NO PROBLEM" in report
    assert "No modification is required for the query." in report


def test_generate_report_for_added_table():

    result = {
        "tables": ["messages"],
        "columns": ["sender", "message"],
        "impacted_changes": [],
        "affected": False,
        "schema_changes": [
            {
                "type": "added_table",
                "table": "users"
            }
        ],
        "impact_reason": (
            "The query is not affected by the detected schema changes."
        ),
        "execution_status": "NO PROBLEM",
        "execution_reason": (
            "The existing query can continue to work with the new schema."
        ),
        "affected_elements": [],
        "analysis_result": (
            "No modification is required for the query."
        )
    }

    report = generate_report(
        result,
        "database_v1.db",
        "database_v2_added_table.db",
        "SELECT sender, message FROM messages;"
    )

    assert "Added Table" in report
    assert "users" in report
    assert "NO PROBLEM" in report
    assert "No modification is required for the query." in report