import sqlite3
import os
import json
from dotenv import load_dotenv
from datasets import load_dataset

load_dotenv()
DB_PATH = "sqlsense.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def setup_database():
    print("Loading Beaver dataset...")
    data = load_dataset('beaverbench/beaver-table', token=os.getenv('HF_TOKEN'))
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schema_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT,
            column_name TEXT,
            column_type TEXT,
            db_id TEXT
        )
    """)

    for split in ['dw', 'nova', 'neutron']:
        for row in data[split]:
            table_name = row['table_name'].lower()
            columns = json.loads(row['column_names'])
            types = json.loads(row['column_types'])
            db_id = row['db']

            cols_def = ", ".join([f"{c.lower()} TEXT" for c in columns])
            try:
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({cols_def})")
            except Exception:
                pass  

            try:
                example_rows = row.get('example_rows', [])
                if example_rows:
                    rows_data = json.loads(example_rows) if isinstance(example_rows, str) else example_rows
                    if rows_data and len(rows_data) > 0:
                        for data_row in rows_data[:5]:
                            if isinstance(data_row, list):
                                placeholders = ", ".join(["?" for _ in data_row])
                                cursor.execute(f"INSERT OR IGNORE INTO {table_name} VALUES ({placeholders})", data_row)
            except Exception:
                pass

            seen = set()
            for col, dtype in zip(columns, types):
                if col.lower() not in seen:
                    seen.add(col.lower())
                    cursor.execute("""INSERT INTO schema_info (table_name, column_name, column_type, db_id) VALUES (?,?,?,?)""", (table_name, col.lower(), dtype, db_id))

    conn.commit()
    conn.close()
    print(f"Database setup complete")

def get_schema_info():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT table_name, column_name, column_type, db_id FROM schema_info")
    rows = cursor.fetchall()
    conn.close()

    schema = {}
    for table, col, dtype, db_id in rows:
        if table not in schema:
            schema[table] = []
        schema[table].append({"column": col, "type": dtype, "db": db_id})
    return schema

if __name__ == "__main__":
    setup_database()