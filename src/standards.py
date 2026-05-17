import chromadb
from chromadb.utils import embedding_functions

def get_chroma_collection():
    client = chromadb.PersistentClient(path="./chroma_db")
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    collection = client.get_or_create_collection(
        name="coding_standards",
        embedding_function=ef
    )
    
    # Only populate if empty
    if collection.count() == 0:
        standards = [
            {"id": "pep8", "text": "Follow PEP 8 guidelines: use 4 spaces for indentation, max 79 characters per line, use snake_case for variables and functions, use UPPER_CASE for constants."},
            {"id": "security", "text": "Security best practices: validate all user inputs, avoid SQL injection by using parameterized queries, never hardcode credentials, sanitize data before processing."},
            {"id": "efficiency", "text": "Efficiency guidelines: avoid nested loops when possible, use list comprehensions over manual loops, prefer built-in functions, be aware of time and space complexity."},
            {"id": "maintainability", "text": "Maintainability rules: follow DRY principle, keep functions small and single-purpose, use meaningful variable names, add docstrings to all functions."},
            {"id": "correctness", "text": "Correctness checks: handle edge cases like None, empty inputs, and type errors, write defensive code, validate function inputs and outputs."},
            {"id": "pythonic", "text": "Pythonic code: use context managers for file handling, use enumerate instead of range(len()), use zip for parallel iteration, prefer f-strings over concatenation."},
        ]
        collection.add(
            documents=[s["text"] for s in standards],
            ids=[s["id"] for s in standards]
        )
    
    return collection

def retrieve_relevant_standards(code: str, n_results: int = 3) -> str:
    collection = get_chroma_collection()
    results = collection.query(
        query_texts=[code],
        n_results=n_results
    )
    retrieved = results["documents"][0]
    return "\n".join([f"- {doc}" for doc in retrieved])