from analyzer.schema_extractor import extract_schema


def compare_schemas(schema_v1, schema_v2):
    changes = []

    # Check for removed tables
    for table in schema_v1:
        if table not in schema_v2:
            changes.append(f"Removed table: {table}")

    # Check for added tables
    for table in schema_v2:
        if table not in schema_v1:
            changes.append(f"Added table: {table}")

    # Compare columns
    for table in schema_v1:
        if table in schema_v2:

            columns_v1 = schema_v1[table]
            columns_v2 = schema_v2[table]

            # Removed columns
            for column in columns_v1:
                if column not in columns_v2:
                    changes.append(
                        f"Removed column: {table}.{column}"
                    )

            # Added columns
            for column in columns_v2:
                if column not in columns_v1:
                    changes.append(
                        f"Added column: {table}.{column}"
                    )

            # Changed column types
            for column in columns_v1:
                if column in columns_v2:

                    type_v1 = columns_v1[column]
                    type_v2 = columns_v2[column]

                    if type_v1 != type_v2:
                        changes.append(
                            f"Changed column type: "
                            f"{table}.{column} "
                            f"({type_v1} → {type_v2})"
                        )

    return changes

if __name__ == "__main__":
    schema_v1 = extract_schema(
        "../test_data/database_v1.db"
    )

    schema_v2 = extract_schema(
        "../test_data/database_v2.db"
    )

    changes = compare_schemas(schema_v1, schema_v2)

    print("Schema Changes:")

    for change in changes:
        print("-", change)

