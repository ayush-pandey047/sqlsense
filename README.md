# SqlSense 

An enterprise Text-to-SQL API that converts natural language questions into executable SQL queries using FastAPI and Groq LLM.

## System Architecture

User Question
    ↓
Retrieval Layer (sentence-transformers + FAISS)
    ↓
LLM Layer (Groq - LLaMA 3.3 70B)
    ↓   
Validation Layer (sqlparse)
    ↓
Execution Layer (SQLite)
    ↓
FastAPI Response

## Dataset
Uses [Beaver Dataset](https://huggingface.co/collections/beaverbench/beaver-dataset) — a real enterprise text-to-SQL benchmark with 381 tables across 3 databases (dw, nova, neutron).

## Components

- **retrieval.py** — Semantic search using sentence-transformers + FAISS to find relevant tables
- **llm.py** — Groq API (LLaMA 3.3 70B) generates SQL from question + schema context
- **validation.py** — SQL syntax validation using sqlparse
- **execution.py** — Executes SQL on SQLite database
- **benchmark.py** — Evaluates system performance on 10 benchmark questions

## API Endpoints

### POST /retrieve
Finds relevant tables for a natural language question.
```json
Input:  { "question": "show me all departments" }
Output: { "retrieved_tables": [...], "scores": [...], "confidence": 0.46 }
```

### POST /generate-sql
Generates SQL from natural language using retrieval + LLM pipeline.
```json
Input:  { "question": "show me all departments", "use_retrieved_context": true }
Output: { "sql": "SELECT...", "is_valid_syntax": true, "execution_results": [...] }
```

### POST /benchmark
Evaluates system performance on benchmark dataset.
```json
Output: { "retrieval_recall": 0.7, "parsing_success_rate": 1.0, "execution_success_rate": 1.0 }
```

## Setup & Installation

```bash
# Clone repo
git clone https://github.com/TERA_USERNAME/sqlsense.git
cd sqlsense

# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add API keys in .env
GROQ_API_KEY=your_groq_key
HF_TOKEN=your_huggingface_token

# Setup database
python3 database.py

# Run server
uvicorn main:app --reload
```

## Access API
Open `http://localhost:8000/docs` in browser.

## Performance
| Metric | Score |
|--------|-------|
| Retrieval Recall | 70% |
| Parsing Success | 100% |
| Execution Success | 100% |
| Avg Latency | ~1.3s |

## Tech Stack
- **FastAPI** — API framework
- **Groq** — LLM inference (LLaMA 3.3 70B)
- **Sentence Transformers** — Semantic search
- **FAISS** — Vector similarity search
- **SQLite** — Database
- **Beaver Dataset** — Enterprise text-to-SQL benchmark