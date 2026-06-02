import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_prompt(question: str, retrieved_tables: list, schema: dict) -> str:
    schema_str = ""
    for item in retrieved_tables:
        table = item["table"]
        if table in schema:
            cols = ", ".join([f"{c['column']} ({c['type']})" for c in schema[table]])
            schema_str += f"\nTable: {table}\nColumns: {cols}\n"

    prompt = f"""You are an expert SQL generator. Generate a valid SQLite SQL query.

Database Schema:
{schema_str}

Question: {question}

Rules:
- Return ONLY the SQL query, no explanation
- Use only the tables and columns provided
- Make sure the SQL is valid SQLite syntax

SQL:"""
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

        return {"sql": sql, "prompt_used": prompt, "error": None}

    except Exception as e:
        print("ERROR:", str(e))
        return {"sql": None, "prompt_used": prompt, "error": str(e)}