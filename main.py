from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from app.retrieval import retrieve_tables
from app.llm import generate_sql
from app.validation import full_validation
from app.execution import execute_sql
from app.benchmark import run_benchmark
from database import get_schema_info, setup_database

app = FastAPI(title="SqlSense", description="Natural Language to SQL API")

@app.on_event("startup")
async def startup():
    setup_database()

class QuestionRequest(BaseModel):
    question: str

    @field_validator('question')
    @classmethod
    def question_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Question cannot be empty")
        if len(v) > 500:
            raise ValueError("Question too long")
        return v

class GenerateRequest(BaseModel):
    question: str
    use_retrieved_context: bool = True

    @field_validator('question')
    @classmethod
    def question_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Question cannot be empty")
        return v

@app.post("/retrieve")
async def retrieve(request: QuestionRequest):
    try:
        results = retrieve_tables(request.question)
        return {
            "retrieved_tables": [r["table"] for r in results],
            "scores": [r["score"] for r in results],
            "confidence": round(sum(r["score"] for r in results) / len(results), 2),
            "details": {r["table"]: {"relevance_score": r["score"], "reason": r["reason"]} for r in results}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-sql")
async def generate(request: GenerateRequest):
    try:
        schema = get_schema_info()
        retrieved = retrieve_tables(request.question) if request.use_retrieved_context else []
        result = generate_sql(request.question, retrieved, schema)
        validation = full_validation(result["sql"], schema) if result["sql"] else {"is_valid_syntax": False, "parsing_errors": "No SQL generated"}
        execution = execute_sql(result["sql"]) if validation["is_valid_syntax"] else {"success": False, "results": []}

        return {
            "sql": result["sql"],
            "retrieved_tables": [r["table"] for r in retrieved],
            "is_valid_syntax": validation["is_valid_syntax"],
            "parsing_errors": validation["parsing_errors"],
            "execution_results": execution["results"],
            "confidence": round(sum(r["score"] for r in retrieved) / len(retrieved), 2) if retrieved else 0,
            "prompt_used": result["prompt_used"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/benchmark")
async def benchmark():
    try:
        return run_benchmark()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))