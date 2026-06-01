import sqlite3
import json
import os
from database import load_dataset

DB_PATH = 'sqlsense.db'

def get_connection():
    return sqlite3.connect(DB_PATH)

def setup_database():
    print('Loading dataset...')
    dataset = load_dataset("yale-lily/spider", trust_remote_code = True)

    conn = get_connection()
    cusour = conn.cursor()

    cusour.execute(""" 
        CREATE TABLE IF NOT EXISTS schema_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT,
            column_name TEXT,
            column_type TEXT,
            db_id TEXT
            )
    """)
    