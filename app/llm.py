import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_prompt(question: str, retrieved_tables: list, schema: dict) -> str:
    schema_str = ""
    for item in retrieved_tables:
        table = item["table"]
        if table in schema:
            seen_cols = set()
            unique_cols = []
            for c in schema[table]:
                if c['column'] not in seen_cols:
                    seen_cols.add(c['column'])
                    unique_cols.append(f"{c['column']} ({c['type']})")
            cols = ", ".join(unique_cols[:10]) 
            schema_str += f"\nTable: {table}\nColumns: {cols}\n"

    examples = """
                Examples:
                Q: Show all department names
                SQL: SELECT DISTINCT department_name FROM sis_department;

                Q: List departments with their school names
                SQL: SELECT department_name, school_name FROM sis_department;

                Q: Show departments that are degree granting
                SQL: SELECT department_name FROM sis_department WHERE is_degree_granting = 'Y';

                Q: Count students per department
                SQL: SELECT department_name, COUNT(*) as total FROM student_department GROUP BY department_name;

                Q: Show space usage for each department
                SQL: SELECT dept_names, sqft, research_volume FROM space_supervisor_usage; """

    prompt = f"""You are an expert SQL generator for enterprise databases. Generate a valid SQLite SQL query.
                        Database Schema:
                            {schema_str}
                            {examples}
                        Now answer this:
                        Q: {question}SQL:"""
    return prompt

def generate_sql(question: str, retrieved_tables: list, schema: dict) -> dict:
    prompt = build_prompt(question, retrieved_tables, schema)

    try:
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1  
        )
        sql = response.choices[0].message.content.strip()
        sql = sql.replace("```sql", "").replace("```", "").strip()
        match = re.search(r'(SELECT|INSERT|UPDATE|DELETE|WITH)[\s\S]+?;', sql, re.IGNORECASE)
        if match:
            sql = match.group(0).strip()


        return {"sql": sql, "prompt_used": prompt, "error": None}

    except Exception as e:
        print("ERROR:", str(e))
        return {"sql": None, "prompt_used": prompt, "error": str(e)}