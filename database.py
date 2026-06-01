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

    for table_name, columns in sample_table.items():
        cols_def = ",".join([f"{col}{dtype}" for col, dtype in columns])
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({cols_def})")

        for col, dtype in columns:
            cusour.execute("""
                INSERT INTO schema_info (table_name, column_name, column_type, db_id)
                VALUES (?, ?, ?, ?)
            """, (table_name, col, dtype, 'university'))

    
    cursor.executemany("INSERT OR IGNORE INTO departments VALUES (?,?,?,?)", [
        (1, "Computer Science", "Tech Block", 500000),
        (2, "Mathematics", "Science Block", 300000),
        (3, "Physics", "Science Block", 250000),
    ])
    
    cursor.executemany("INSERT OR IGNORE INTO enrollments VALUES (?,?,?,?,?)", [
        (1, 101, 1, 150, "Fall2024"),
        (2, 102, 2, 80, "Fall2024"),
        (3, 103, 1, 120, "Spring2024"),
    ])
    
    cursor.executemany("INSERT OR IGNORE INTO courses VALUES (?,?,?,?,?)", [
        (1, "Data Structures", 1, 0, 4),
        (2, "Linear Algebra", 2, 1, 3),
        (3, "Quantum Physics", 3, 0, 4),
    ])