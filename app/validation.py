import sqlparse
import sqlite3
from databse import get_connection

def validate_sql(sql:str) -> dict:
    try:
        parased = sqlparse.parse(sql)
        if not parased or not sql.strip():
            return {'is_valid': False, 'error': 'Empty or invalid SQL syntax.'}
        return {'is_valid': True, 'error': None}
    except Exception as e:
        return {'is_valid': False, 'error': f'SQL syntax error: {str(e)}'}

def validate_table_exists(sql:str, schema:dict) -> dict:
    sql_upper = sql.upper()
    missing_tables = []
    for table in schema.keys():
        if table.upper() in sql_upper:
            if table not in schema:
                missing_tables.append(table)
    
    if missing:
        return {'is_valid': False, 'error': f'Missing tables: {missing}'}

def full_validation(sql:str, schema:dict) -> dict:
    syntax = validate_syntax(sql)
    if not syntax['is_valid']:
        return {'valid': False, 'error': syntax['error']}
    
    tables = validate_table_exists(sql, schema)
    return {
        'is_valid_syntax': True,
        'parising_errors': tables['error'] if not tables['is_valid'] else None
    }