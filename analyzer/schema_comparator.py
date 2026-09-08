from analyzer.schema_extractor import extract_schema


def compare_schemas(schema_v1, schema_v2):
    changes = []

    # Check for removed tables
    for table in schema_v1:
        if table not in schema_v2:
            changes.append({
                "type": "removed_table",
                "table": table
            })

    # Check for added tables
    for table in schema_v2:
        if table not in schema_v1:
            changes.append({
                "type": "added_table",
                "table": table
            })

    # Compare columns
    for table in schema_v1:
        if table in schema_v2:
            columns_v1 = schema_v1[table]
            columns_v2 = schema_v2[table]

            # Removed columns
            for column in columns_v1:
                if column not in columns_v2:
                    changes.append({
                        "type": "removed_column",
                        "table": table,
                        "column": column
                    })

            # Added columns
            for column in columns_v2:
                if column not in columns_v1:
                    changes.append({
                        "type": "added_column",
                        "table": table,
                        "column": column
                    })

            # Changed column types
            for column in columns_v1:
                if column in columns_v2:
                    type_v1 = columns_v1[column]
                    type_v2 = columns_v2[column]

                    if type_v1 != type_v2:
                        changes.append({
                            "type": "changed_column_type",
                            "table": table,
                            "column": column,
                            "old_type": type_v1,
                            "new_type": type_v2
                        })

    return changes
