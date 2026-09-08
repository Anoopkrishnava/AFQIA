from analyzer.schema_extractor import extract_schema
from analyzer.schema_comparator import compare_schemas
from analyzer.query_analyzer import analyze_query_impact


# Database files
old_db = "old_database.db"
new_db = "new_database.db"


# Extract schemas from actual SQLite databases
schema_v1 = extract_schema(old_db)
schema_v2 = extract_schema(new_db)


# Compare database schemas
changes = compare_schemas(schema_v1, schema_v2)


# Old forensic query
query = """
SELECT sender, message
FROM messages;
"""


# Analyze query impact
result = analyze_query_impact(query, changes)


print("=" * 60)
print("       AFQIA - FORENSIC QUERY IMPACT ANALYSIS")
print("=" * 60)


print("\nOLD DATABASE SCHEMA")
print("-" * 60)

for table, columns in schema_v1.items():
    print(table)
    for column, data_type in columns.items():
        print(f"  {column:<12} {data_type}")


print("\nNEW DATABASE SCHEMA")
print("-" * 60)

for table, columns in schema_v2.items():
    print(table)
    for column, data_type in columns.items():
        print(f"  {column:<12} {data_type}")


print("\nSCHEMA CHANGES")
print("-" * 60)

for change in changes:

    if change["type"] == "removed_column":
        print(
            f"[REMOVED]  "
            f"{change['table']}.{change['column']}"
        )

    elif change["type"] == "added_column":
        print(
            f"[ADDED]    "
            f"{change['table']}.{change['column']}"
        )

    elif change["type"] == "removed_table":
        print(
            f"[REMOVED TABLE] "
            f"{change['table']}"
        )

    elif change["type"] == "added_table":
        print(
            f"[ADDED TABLE]   "
            f"{change['table']}"
        )

    elif change["type"] == "changed_column_type":
        print(
            f"[TYPE CHANGED] "
            f"{change['table']}.{change['column']} "
            f"({change['old_type']} -> {change['new_type']})"
        )


print("\nFORENSIC QUERY")
print("-" * 60)
print(query.strip())


print("\nQUERY DEPENDENCIES")
print("-" * 60)
print("Tables :", ", ".join(result["tables"]))
print("Columns:", ", ".join(result["columns"]))


print("\nIMPACT ANALYSIS")
print("-" * 60)

if result["impacted_changes"]:

    print("Affected components:")

    for change in result["impacted_changes"]:

        if "column" in change:
            print(
                f"  - {change['table']}.{change['column']}"
            )
        else:
            print(
                f"  - {change['table']}"
            )

else:
    print("No affected components.")


print("\nImpact Level  :", result["impact_level"])
print("Execution Risk:", result["execution_risk"])

print("\n" + "=" * 60)
