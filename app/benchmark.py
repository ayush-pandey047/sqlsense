import time
from app.retrieval import retrieve_tables
from app.llm import generate_sql
from app.validation import full_validation
from app.execution import execute_sql
from database import get_schema_info

BENCHMARK_QUESTIONS = [
    {"question": "Show all departments", "expected_tables": ["sis_department"]},
    {"question": "List all students in a department", "expected_tables": ["student_department"]},
    {"question": "Show department names and school names", "expected_tables": ["sis_department"]},
    {"question": "Which departments are degree granting?", "expected_tables": ["sis_department"]},
    {"question": "Show space usage by department", "expected_tables": ["space_supervisor_usage"]},
    {"question": "List department codes and full names", "expected_tables": ["sis_department"]},
    {"question": "Show departments with their school codes", "expected_tables": ["student_department"]},
    {"question": "Which departments have supervisors?", "expected_tables": ["space_supervisor_usage"]},
    {"question": "Show department budget codes", "expected_tables": ["sis_department"]},
    {"question": "List all school names", "expected_tables": ["sis_department"]},
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
