import sqlite3
from database import get_connection

def execute_sql(sql: str) -> dict:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        conn.close()

        results = [dict(zip(columns, row)) for row in rows]
        return {'sucess':True, 'results': results, 'error': None}

    except Exception as e:
        return {'sucess':False, 'results': None, 'error': str(e)}
