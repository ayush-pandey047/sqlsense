import os 
from groq import Groq 
from dotenv import load_dotenv 

load_dotenv()

client = Groq(api_key = os.getenv("GROQ_API_KEY"))

def build_prompt(question:str, retrieve_tables: list, schema: dict) -> str:
    schema_desc = ""
    schema_str = ""  
    for item in retrieve_tables:
        table_name = item["table"]
        if table_name in schema:  
            cols = ", ".join([f"{c['column']} ({c['type']})" for c in schema[table_name]])
            schema_str += f"\nTable: {table_name}\nColumns: {cols}\n"
    
    prompt = f"""You are an expert SQL generator. Given the following database schema and a natural language question, generate an accurate SQL query."""
    
Database Schema:
{schema_str}

Question: {question}

Rules: 
-Return ONLY the SQL query, no explanations.
-Use only the tables and columns provided schema.
-Make sure the SQL is valid SQLite syntax.

SQL:"""
    return prompt

def generate_sql(question: str, retrieved_tables: list, schema: dict) -> dict:
    prompt = build_prompt(question, retrieved_tables, schema)

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1 
        )
        sql = response.choices[0].message.content.strip()

        return {"sql": sql, "prompt_used": prompt, "error": None}

    except Exception as e:
        return {"sql": None, "prompt_used": prompt, "error": str(e)}