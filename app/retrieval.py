import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np 
from database import get_schema_info

model = SentenceTransformer('all-MiniLM-L6-v2')

def build_index(db_id):
    tables = []
    descriptions = []

    for table, columns in schema.items():
        cols = ','.join([c['column'] for c in columns])
        desc = f"{table_name}:{cols}"
        tables.append(table_name)
        descriptions.append(desc)
    
    embeddings = model.encode(descriptions)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    return index, tables, descriptions


def retrieve_tables