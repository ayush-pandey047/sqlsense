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


            for col, dtype in zip(columns, types):
                cursor.execute("""
                    INSERT INTO schema_info (table_name, column_name, column_type, db_id)
                    VALUES (?,?,?,?)
                """, (table_name, col.lower(), dtype, db_id))

    conn.commit()
    conn.close()
    print(f"Database setup complete")
