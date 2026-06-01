import sqlite3
import json
import os

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

    sample_table = {
        'departments': [
            ('dept_id', 'INTEGER'),
            ('dept_name', 'TEXT')
            ('building', 'TEXT'),
            ('budget', 'REAL')
        ],
        'enrollments':[
            ('enrollement_id', 'INTEGER'),
            ('student_id', 'INTEGER'),
            ('dept_id', 'INTEGER'),
            ('student_count', 'INTEGER'),
            ('semester', 'TEXT')
        ],
        'courses': [
            ('course_id', 'INTEGER'),
            ('course_name', 'TEXT'),
            ('dept_id', 'INTEGER'),
            ('its_online', 'INTEGER'),
            ('credits', 'INTEGER')
        ],
        'students': [
            ('student_id', 'INTEGER'),
            ('name', 'TEXT'),
            ('age', 'INTEGER'),
            ('dept_id', 'INTEGER'),
            ('gpa', 'REAL')
        ],
        'instructors': [
            ('instructor_id', 'INTEGER'),
            ('name', 'TEXT'),
            ('dept_id', 'INTEGER'),
            ('salary', 'REAL')
        ]
    }

