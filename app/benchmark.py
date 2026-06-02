import time
from app.retrieval import retrieve_tables
from app.llm import generate_sql
from app.validation import full_validation
from app.execution import execute_sql
from database import get_schema_info

BENCHMARK_QUESTIONS = [
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
    total = len(BENCHMARK_QUESTIONS)
    
    retrieval_success = 0
    parsing_success = 0
    execution_success = 0
    total_latency = 0

    for item in BENCHMARK_QUESTIONS:
        question = item["question"]
        expected = item["expected_tables"]
        start = time.time()

        retrieved = retrieve_tables(question)
        retrieved_names = [r["table"] for r in retrieved]
        
        matched = len(set(expected) & set(retrieved_names))
        if matched == len(expected):
            retrieval_success += 1

        result = generate_sql(question, retrieved, schema)
        sql = result["sql"]

        if sql:
            validation = full_validation(sql, schema)
            if validation["is_valid_syntax"]:
                parsing_success += 1

            execution = execute_sql(sql)
            if execution["success"]:
                execution_success += 1

        total_latency += (time.time() - start) * 1000

    return {
        "total_queries": total,
        "metrics": {
            "retrieval_recall": round(retrieval_success / total, 2),
            "parsing_success_rate": round(parsing_success / total, 2),
            "execution_success_rate": round(execution_success / total, 2),
            "average_latency_ms": round(total_latency / total, 2)
        },
        "error_analysis": {
            "retrieval_failures": total - retrieval_success,
            "parsing_failures": total - parsing_success,
            "execution_failures": total - execution_success
        }
    }
