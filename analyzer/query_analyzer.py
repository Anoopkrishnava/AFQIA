import re
import sqlite3



def validate_query(db_path, query):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("EXPLAIN " + query)

        connection.close()

        return True, None

    except sqlite3.Error as error:
        return False, str(error)



def analyze_query(query):
    tables = []
    columns = []

    # Find table and optional alias after FROM
    from_match = re.search(
        r'\bFROM\s+(\w+)(?:\s+(?:AS\s+)?(\w+))?',
        query,
        re.IGNORECASE
    )

    alias = None

    if from_match:
        table_name = from_match.group(1)
        alias = from_match.group(2)

        tables.append(table_name)

        join_tables = re.findall(
            r'\bJOIN\s+(\w+)',
            query,
            re.IGNORECASE
        )

        for table in join_tables:
            if table not in tables:
                tables.append(table)

    # Find columns after SELECT
    select_match = re.search(
        r'\bSELECT\s+(.*?)\s+FROM',
        query,
        re.IGNORECASE
    )

    if select_match:
        selected_columns = select_match.group(1).split(",")

        for column in selected_columns:
            column = column.strip()

            # Remove table alias
            if "." in column:
                column = column.split(".")[-1]

            if column != "*":
                columns.append(column)

    # Find columns used in WHERE
    where_match = re.search(
        r'\bWHERE\s+(.*?)(?:;|$)',
        query,
        re.IGNORECASE
    )

    if where_match:
        where_clause = where_match.group(1)

        where_columns = re.findall(
            r'(?:\b\w+\.)?([A-Za-z_][A-Za-z0-9_]*)\s*'
            r'(?:=|>|<|>=|<=|LIKE|IN)',
            where_clause,
            re.IGNORECASE
        )

        for column in where_columns:
            if column not in columns:
                columns.append(column)
                
        # Find columns used in JOIN conditions
    join_conditions = re.findall(
        r'\bJOIN\s+\w+(?:\s+(?:AS\s+)?\w+)?\s+ON\s+(.*?)(?=\bJOIN\b|\bWHERE\b|;|$)',
        query,
        re.IGNORECASE
    )

    for condition in join_conditions:
        join_columns = re.findall(
            r'(?:\b\w+\.)?([A-Za-z_][A-Za-z0-9_]*)\s*(?:=|>|<|>=|<=)',
            condition,
            re.IGNORECASE
        )

        for column in join_columns:
            if column not in columns:
                columns.append(column)

    return {
        "tables": tables,
        "columns": columns
    }

def check_query_impact(query, changes):
    analysis = analyze_query(query)

    impacted = []

    # Build table-to-alias mapping
    table_aliases = {}

    from_match = re.search(
        r'\bFROM\s+(\w+)(?:\s+(?:AS\s+)?(\w+))?',
        query,
        re.IGNORECASE
    )

    if from_match:
        table_name = from_match.group(1)
        alias = from_match.group(2)

        table_aliases[table_name] = alias if alias else table_name

    join_matches = re.findall(
        r'\bJOIN\s+(\w+)(?:\s+(?:AS\s+)?(\w+))?',
        query,
        re.IGNORECASE
    )

    for table_name, alias in join_matches:
        table_aliases[table_name] = alias if alias else table_name

    for change in changes:
        for table in analysis["tables"]:

            # Removed table
            if change["type"] == "removed_table":
                if change["table"] == table:
                    impacted.append(change)

            # Column-related changes
            elif change["table"] == table:

                column = change["column"]

                # Check normal/unqualified column usage
                if column in analysis["columns"]:
                    impacted.append(change)
                    continue

                # Check qualified column usage through table alias
                alias = table_aliases.get(table)

                if alias:
                    qualified_column = alias + "." + column

                    if re.search(
                        rf'\b{re.escape(qualified_column)}\b',
                        query,
                        re.IGNORECASE
                    ):
                        impacted.append(change)

    return impacted
    

    

def get_execution_risk(query, changes):
    impacted = check_query_impact(query, changes)

    if not impacted:
        return "NONE"

    for change in impacted:
        if change["type"] in [
            "removed_table",
            "removed_column"
        ]:
            return "BREAKING"

        if change["type"] == "changed_column_type":
            return "AFFECTED"

    return "NONE"

def analyze_query_impact(query, changes):
    analysis = analyze_query(query)
    impacted = check_query_impact(query, changes)

    affected = len(impacted) > 0

    return {
        "tables": analysis["tables"],
        "columns": analysis["columns"],
        "impacted_changes": impacted,
        "affected": affected
    }
