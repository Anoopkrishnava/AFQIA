def generate_report(result, old_db, new_db, query):
    report = []

    report.append("=" * 50)
    report.append("          AFQIA – QUERY IMPACT ANALYSIS")
    report.append("=" * 50)

    report.append("")
    report.append("OLD DATABASE:")
    report.append(old_db)

    report.append("")
    report.append("NEW DATABASE:")
    report.append(new_db)

    report.append("")
    report.append("FORENSIC QUERY:")
    report.append(query)

    report.append("")
    report.append("-" * 50)
    report.append("1. SCHEMA CHANGES")
    report.append("-" * 50)

    for change in result["schema_changes"]:
        change_names = {
        "removed_table": "Removed Table",
        "added_table": "Added Table",
        "removed_column": "Removed Column",
        "added_column": "Added Column",
        "changed_column_type": "Changed Column Type"
        }

        change_type = change_names.get(
            change["type"],
            change["type"]
            )

        report.append(f"Change Type : {change_type}")
        report.append(f"Table       : {change['table']}")

        if "column" in change:
            report.append(f"Column      : {change['column']}")

        if "old_type" in change:
            report.append(f"Old Type    : {change['old_type']}")

        if "new_type" in change:
            report.append(f"New Type    : {change['new_type']}")

        report.append("")

    report.append("-" * 50)
    report.append("2. QUERY DEPENDENCIES")
    report.append("-" * 50)

    report.append("")
    report.append("Tables Used:")

    for table in result["tables"]:
        report.append(f"- {table}")

    report.append("")
    report.append("Columns Used:")

    for column in result["columns"]:
        report.append(f"- {column}")


    report.append("")
    report.append("-" * 50)
    report.append("3. QUERY IMPACT")
    report.append("-" * 50)

    report.append("")
    report.append(
        f"Affected: {'YES' if result['affected'] else 'NO'}"
    )

    report.append("")
    report.append("Reason:")
    report.append(result["impact_reason"])

    report.append("")
    report.append("-" * 50)
    report.append("4. QUERY EXECUTION")
    report.append("-" * 50)

    report.append("")
    report.append(f"Status: {result['execution_status']}")
    report.append("")
    report.append("Reason:")
    report.append(result["execution_reason"])


    report.append("")
    report.append("-" * 50)
    report.append("5. AFFECTED QUERY ELEMENTS")
    report.append("-" * 50)

    report.append("")

    if result["affected_elements"]:
        for element in result["affected_elements"]:
            report.append(element)
    else:
        report.append("None")


    report.append("")
    report.append("-" * 50)
    report.append("6. ANALYSIS RESULT")
    report.append("-" * 50)

    report.append("")
    report.append(result["analysis_result"])

    return "\n".join(report)