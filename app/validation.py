import sqlparse
import sqlite3
from database import get_connection

def validate_syntax(sql: str) -> dict:
    try:
        parsed = sqlparse.parse(sql)
        if not parsed or not sql.strip():
            return {"is_valid": False, "error": "Empty or invalid SQL"}
        return {"is_valid": True, "error": None}
    except Exception as e:
        return {"is_valid": False, "error": str(e)}

def validate_tables_exist(sql: str, schema: dict) -> dict:
    sql_upper = sql.upper()
    missing = []
    for table in schema.keys():
        if table.upper() in sql_upper:
            if table not in schema:
                missing.append(table)
    
    if missing:
        return {"is_valid": False, "error": f"Tables not found: {missing}"}
    return {"is_valid": True, "error": None}

def full_validation(sql: str, schema: dict) -> dict:
    syntax = validate_syntax(sql)
    if not syntax["is_valid"]:
        return {"is_valid_syntax": False, "parsing_errors": syntax["error"]}
    
    tables = validate_tables_exist(sql, schema)
    return {
        "is_valid_syntax": True,
        "parsing_errors": tables["error"] if not tables["is_valid"] else None
    }