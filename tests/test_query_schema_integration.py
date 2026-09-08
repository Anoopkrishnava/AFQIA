from analyzer.schema_extractor import extract_schema
from analyzer.schema_comparator import compare_schemas
from analyzer.query_analyzer import check_query_impact


def test_query_schema_impact():
    schema_v1 = extract_schema(
        "test_data/database_v1.db"
    )

    schema_v2 = extract_schema(
        "test_data/database_v2_removed_column.db"
    )

    changes = compare_schemas(
        schema_v1,
        schema_v2
    )

    query = """
    SELECT sender, message
    FROM messages;
    """

    impacted = check_query_impact(
        query,
        changes
    )

    assert {
        "type": "removed_column",
        "table": "messages",
        "column": "message"
    } in impacted
    
