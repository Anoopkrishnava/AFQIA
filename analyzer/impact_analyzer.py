from analyzer.schema_extractor import extract_schema
from analyzer.schema_comparator import compare_schemas
from analyzer.query_analyzer import analyze_query_impact


def get_impact_reason(impacted_changes):
    if not impacted_changes:
        return (
            "No detected schema change affects the identified "
            "query dependencies. This does not guarantee that "
            "the query retrieves all intended forensic evidence."
        )

    reasons = []

    for change in impacted_changes:
        change_type = change["type"]

        if change_type == "removed_table":
            table = change["table"]
            reasons.append(
                f"The table '{table}' was removed from the new "
                f"database schema. The query depends on this table, "
                f"so the query may fail. Recommended action: inspect "
                f"the new schema to determine whether the required "
                f"data is stored in another table."
            )

        elif change_type == "removed_column":
            table = change["table"]
            column = change["column"]
            reasons.append(
                f"The column (attribute) '{column}' in the table "
                f"'{table}' was removed from the new database schema. "
                f"The query references this missing column, so "
                f"execution will fail if that reference is used. "
                f"Recommended action: inspect the columns of table "
                f"'{table}' and determine whether the required "
                f"evidence is available under another column or table."
            )

        elif change_type == "changed_column_type":
            table = change["table"]
            column = change["column"]
            old_type = change["old_type"]
            new_type = change["new_type"]
            reasons.append(
                f"The datatype of column (attribute) '{column}' in "
                f"table '{table}' changed from '{old_type}' to "
                f"'{new_type}'. The query may still execute, but "
                f"comparisons, filtering, sorting, or interpretation "
                f"of values may change. Recommended action: inspect "
                f"the new values and verify that the query's conditions "
                f"and results remain appropriate."
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
        change_type = change["type"]

        if change_type == "removed_table":
            elements.append(
                f"Table: '{change['table']}' (removed)"
            )

        elif change_type == "added_table":
            elements.append(
                f"Table: '{change['table']}' (added)"
            )

        elif change_type == "removed_column":
            elements.append(
                f"Column (attribute): '{change['column']}' "
                f"in table '{change['table']}' (removed)"
            )

        elif change_type == "added_column":
            elements.append(
                f"Column (attribute): '{change['column']}' "
                f"in table '{change['table']}' (added)"
            )

        elif change_type == "changed_column_type":
            elements.append(
                f"Column (attribute): '{change['column']}' "
                f"in table '{change['table']}' "
                f"(datatype changed from '{change['old_type']}' "
                f"to '{change['new_type']}')"
            )

    return elements


def get_analysis_result(impacted_changes):
    if not impacted_changes:
        return (
            "The original query has no detected schema-related impact. "
            "However, review the Evidence Completeness Review section "
            "to determine whether newly added tables or columns contain "
            "relevant forensic evidence."
        )

    recommendations = []

    for change in impacted_changes:
        change_type = change["type"]

        if change_type == "removed_table":
            table = change["table"]
            recommendations.append(
                f"Inspect the new schema to determine whether the "
                f"required evidence from the removed table '{table}' "
                f"is available in another table. Update the query "
                f"manually only after verifying the alternative source."
            )

        elif change_type == "removed_column":
            table = change["table"]
            column = change["column"]
            recommendations.append(
                f"The query references the removed column (attribute) "
                f"'{column}' in table '{table}'. Inspect the new schema "
                f"to identify whether the required data is available "
                f"under another column or table, then update the query "
                f"manually if appropriate."
            )

        elif change_type == "changed_column_type":
            table = change["table"]
            column = change["column"]
            old_type = change["old_type"]
            new_type = change["new_type"]
            recommendations.append(
                f"Verify how the datatype change of column (attribute) "
                f"'{column}' in table '{table}' from '{old_type}' to "
                f"'{new_type}' affects query conditions and results. "
                f"Test the query and make any necessary changes manually."
            )

        elif change_type == "added_column":
            table = change["table"]
            column = change["column"]
            recommendations.append(
                f"Check whether the added column (attribute) "
                f"'{column}' in table '{table}' contains evidence "
                f"relevant to the investigation. If required, consider "
                f"including it in a manually reviewed query."
            )

        elif change_type == "added_table":
            table = change["table"]
            recommendations.append(
                f"Inspect the added table '{table}' to determine "
                f"whether it contains relevant forensic evidence "
                f"that the original query does not retrieve."
            )

    if not recommendations:
        return (
            "Review the detected schema changes and test the query "
            "against the new database before deciding whether "
            "a manual modification is necessary."
        )

    return " ".join(recommendations)



def get_evidence_completeness_warning(schema_changes, query_tables):
    warnings = []

    for change in schema_changes:
        change_type = change["type"]
        table = change["table"]

        if change_type == "added_column" and table in query_tables:
            column = change["column"]
            warnings.append(
                f"Review whether the added column (attribute) "
                f"'{column}' in table '{table}' contains relevant "
                f"forensic evidence not retrieved by the original query."
            )

        elif change_type == "added_table":
            warnings.append(
                f"Inspect the added table '{table}' to determine "
                f"whether it contains relevant forensic evidence "
                f"that the original query does not retrieve."
            )

    if warnings:
        return " ".join(warnings)

    return (
        "No added tables or columns were detected that require "
        "an evidence-completeness review."
    )




def analyze_database_query(old_db, new_db, query):
    old_schema = extract_schema(old_db)
    new_schema = extract_schema(new_db)

    changes = compare_schemas(old_schema, new_schema)

    # Schema-only analysis when no query is provided
    if not query:
        return {
            "old_schema": old_schema,
            "new_schema": new_schema,
            "schema_changes": changes,
            "tables": [],
            "columns": [],
            "affected": False,
            "impact_reason": "",
            "execution_status": "",
            "execution_reason": "",
            "affected_elements": [],
            "analysis_result": ""
        }

    # Query impact analysis when a query is provided
    result = analyze_query_impact(query, changes)

    result["schema_changes"] = changes

    result["evidence_completeness_warning"] = (
        get_evidence_completeness_warning(
            changes,
            result["tables"]
        )
    )

    result["impact_reason"] = get_impact_reason(
        result["impacted_changes"]
    )

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

    result["old_schema"] = old_schema
    result["new_schema"] = new_schema

    return result


def get_execution_reason(impacted_changes):
    if not impacted_changes:
        return (
            "No detected schema change prevents the identified query "
            "from working. The query should still be tested against "
            "the new database, and its results must be checked for "
            "forensic completeness."
        )

    reasons = []

    for change in impacted_changes:
        change_type = change["type"]

        if change_type == "removed_table":
            table = change["table"]
            reasons.append(
                f"Execution is expected to fail if the query references "
                f"the removed table '{table}'. Inspect the new schema "
                f"for a possible alternative data source before manually "
                f"updating the query."
            )

        elif change_type == "removed_column":
            table = change["table"]
            column = change["column"]
            reasons.append(
                f"Execution is expected to fail because the query "
                f"references the removed column (attribute) '{column}' "
                f"in table '{table}'. Inspect the new schema and verify "
                f"where the required evidence is stored before manually "
                f"changing the query."
            )

        elif change_type == "changed_column_type":
            table = change["table"]
            column = change["column"]
            old_type = change["old_type"]
            new_type = change["new_type"]
            reasons.append(
                f"The datatype of column (attribute) '{column}' in "
                f"table '{table}' changed from '{old_type}' to "
                f"'{new_type}'. The query may execute, but its filtering, "
                f"comparison, sorting, or interpretation of values may "
                f"differ. Test the query and verify its results."
            )

    return " ".join(reasons)