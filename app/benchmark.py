import time 
from app.retrieval import retrieve_tables
from app.llm import generate_sql
from app.validation import full_validation
from app.execution import execute_sql
from database import get_schema_info

BENCHMARK_QUESTION = [
    {"question": "Show all departments", "expected_tables": ["departments"]},
    {"question": "Which departments have more than 100 students?", "expected_tables": ["departments", "enrollments"]},
    {"question": "List all online courses", "expected_tables": ["courses"]},
    {"question": "Show students with GPA above 3.5", "expected_tables": ["students"]},
    {"question": "Which instructors earn more than 50000?", "expected_tables": ["instructors"]},
    {"question": "Count students per department", "expected_tables": ["departments", "enrollments"]},
    {"question": "Show all courses with credits more than 3", "expected_tables": ["courses"]},
    {"question": "List departments with their buildings", "expected_tables": ["departments"]},
    {"question": "Show enrolled students in Fall2024", "expected_tables": ["enrollments"]},
    {"question": "Which students are in Computer Science?", "expected_tables": ["students", "departments"]},
]

def run_benchmark():
    schema = get_schema_info()
    total = len(BENCHMARK_QUESTION)

    retrieval_success = 0
    parsing_success = 0
    execution_success = 0
    total_latency = 0

