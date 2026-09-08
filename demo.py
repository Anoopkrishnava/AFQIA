from analyzer.schema_comparator import compare_schemas
from analyzer.query_analyzer import analyze_query_impact


# Old database schema
schema_v1 = {
    "messages": {
        "id": "INTEGER",
        "sender": "TEXT",
        "message": "TEXT"
    }
}

# New database schema
schema_v2 = {
    "messages": {
        "id": "INTEGER",
        "sender": "TEXT",
        "content": "TEXT",
        "timestamp": "TEXT"
    }
}

# Old forensic query
query = """
SELECT sender, message
FROM messages;
"""


# 1. Compare database schemas
changes = compare_schemas(schema_v1, schema_v2)

# 2. Analyze query impact
result = analyze_query_impact(query, changes)


print("=" * 60)
print("       AFQIA - FORENSIC QUERY IMPACT ANALYSIS")
print("=" * 60)

print("\nOLD DATABASE SCHEMA")
print("-" * 60)

for table, columns in schema_v1.items():
    print(f"{table}")
    for column, data_type in columns.items():
        print(f"  {column:<12} {data_type}")

print("\nNEW DATABASE SCHEMA")
print("-" * 60)

for table, columns in schema_v2.items():
    print(f"{table}")
    for column, data_type in columns.items():
        print(f"  {column:<12} {data_type}")

print("\nSCHEMA CHANGES")
print("-" * 60)

for change in changes:

    if change["type"] == "added_column":
        print(
            f"[ADDED]    {change['table']}.{change['column']}"
        )

    elif change["type"] == "removed_column":
        print(
            f"[REMOVED]  {change['table']}.{change['column']}"
        )

    elif change["type"] == "added_table":
        print(
            f"[ADDED TABLE]    {change['table']}"
        )

    elif change["type"] == "removed_table":
        print(
            f"[REMOVED TABLE]  {change['table']}"
        )

    elif change["type"] == "changed_column_type":
        print(
            f"[TYPE CHANGED] {change['table']}."
            f"{change['column']} "
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

for change in result["impacted_changes"]:
    if change["type"] == "removed_column":
        print(
            f"Affected: {change['table']}.{change['column']}"
        )

print(f"Impact Level  : {result['impact_level']}")
print(f"Execution Risk: {result['execution_risk']}")

print("\n" + "=" * 60)
