import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from database import get_schema_info

model = SentenceTransformer('all-MiniLM-L6-v2')

def build_descriptions(schema: dict):
    name_words = table_name.replace("_", " ").lower()
    col_names = ", ".join([c['column'].replace("_", " ") for c in columns])
    return f"{name_words}. Columns: {col_names}. Table about {name_words}."

def build_index(schema: dict):
    tables = []
    descriptions = []

    for table_name, columns in schema.items():
        cols = ", ".join([c['column'] for c in columns])
        desc = f"{table_name}: {cols}"
        tables.append(table_name)
        descriptions.append(desc)


    embeddings = model.encode(descriptions)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    return index, tables, descriptions

def retrieve_tables(question: str, top_k: int = 5):
    schema = get_schema_info()
    index, tables, descriptions = build_index(schema)

 
    question_vec = model.encode([question])
    distances, indices = index.search(np.array(question_vec), top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        score = float(1 / (1 + distances[0][i]))
        results.append({
            "table": tables[idx],
            "score": round(score, 4),
            "reason": f"Matched with: {descriptions[idx]}"
        })

    return results