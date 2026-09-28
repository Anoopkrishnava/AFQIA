from analyzer.schema_extractor import extract_schema
from analyzer.schema_comparator import compare_schemas
from analyzer.query_analyzer import analyze_query_impact


def get_impact_reason(impacted_changes):
    if not impacted_changes:
        return "The query is not affected by the detected schema changes."

    reasons = []

    for change in impacted_changes:
        if change["type"] == "removed_table":
            reasons.append(
                f"The query uses table '{change['table']}', "
                f"which was removed from the new database schema."
            )

        elif change["type"] == "removed_column":
            reasons.append(
                f"The query uses column '{change['table']}.{change['column']}', "
                f"which was removed from the new database schema."
            )

        elif change["type"] == "changed_column_type":
            reasons.append(
                f"The query uses column '{change['table']}.{change['column']}', "
                f"whose type changed from {change['old_type']} "
                f"to {change['new_type']}."
            )

    return " ".join(reasons)


def get_execution_status(impacted_changes):
    if not impacted_changes:
        return "NO PROBLEM"

    for change in impacted_changes:
        if change["type"] in ["removed_table", "removed_column"]:
            return "WILL FAIL"

    return "REQUIRES REVIEW"


def get_affected_elements(impacted_changes):
    elements = []

    for change in impacted_changes:
        if change["type"] == "removed_table":
            elements.append(change["table"])

        elif change["type"] in ["removed_column", "added_column",
                                "changed_column_type"]:
            elements.append(
                f"{change['table']}.{change['column']}"
            )

    return elements


def get_analysis_result(impacted_changes):
    if not impacted_changes:
        return "No modification is required for the query."

    for change in impacted_changes:
        if change["type"] in ["removed_table", "removed_column"]:
            return "Query modification is required."

    return "Further analyst review is required."


def analyze_database_query(old_db, new_db, query):
    old_schema = extract_schema(old_db)
    new_schema = extract_schema(new_db)

    changes = compare_schemas(old_schema, new_schema)

    result = analyze_query_impact(query, changes)

    result["schema_changes"] = changes

    result["impact_reason"] = get_impact_reason(result["impacted_changes"])

    result["execution_status"] = get_execution_status(
        result["impacted_changes"]
    )
    result["execution_reason"] = get_execution_reason(
        result["impacted_changes"]
    )
    result["affected_elements"] = get_affected_elements(
        result["impacted_changes"]
    )
    result["analysis_result"] = get_analysis_result(
        result["impacted_changes"]
    )

    return result


def get_execution_reason(impacted_changes):
    if not impacted_changes:
        return "The existing query can continue to work with the new schema."

    for change in impacted_changes:
        if change["type"] == "removed_table":
            return (
                f"The table '{change['table']}' no longer exists "
                "in the new database schema."
            )

        elif change["type"] == "removed_column":
            return (
                f"The column '{change['table']}.{change['column']}' "
                "no longer exists in the new database schema."
            )

        elif change["type"] == "changed_column_type":
            return (
                f"The column '{change['table']}.{change['column']}' "
                f"changed from {change['old_type']} to {change['new_type']}."
            )