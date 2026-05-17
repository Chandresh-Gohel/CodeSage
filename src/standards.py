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
            {"id": "pep8", "text": "PEP 8: use 4 spaces indentation, max 79 chars per line, snake_case for variables, blank lines between functions."},
            {"id": "security_sql", "text": "SQL injection prevention: always use parameterized queries, never concatenate user input directly into SQL strings."},
            {"id": "security_input", "text": "Input validation: validate and sanitize all user inputs, check data types, lengths, and ranges before processing."},
            {"id": "efficiency_loops", "text": "Loop optimization: avoid nested loops O(n²), use list comprehensions, prefer built-in functions like map() and filter()."},
            {"id": "efficiency_ds", "text": "Data structures: use sets for O(1) lookup instead of lists, use dictionaries for key-value pairs, avoid unnecessary copies."},
            {"id": "maintainability_dry", "text": "DRY principle: avoid code duplication, extract repeated logic into helper functions, use constants for repeated values."},
            {"id": "maintainability_solid", "text": "Single responsibility: each function should do one thing only, keep functions under 20 lines, split complex functions."},
            {"id": "pythonic_context", "text": "Use context managers: always use 'with' statement for file operations and database connections to ensure proper cleanup."},
            {"id": "pythonic_comprehension", "text": "List comprehensions: prefer [x for x in items if condition] over manual for loops with append for simple transformations."},
            {"id": "error_handling", "text": "Error handling: use specific exception types not bare except, always handle exceptions gracefully, log errors properly."},
            {"id": "docstrings", "text": "Documentation: every function must have a docstring explaining purpose, parameters, return values, and exceptions raised."},
            {"id": "type_hints", "text": "Type hints: use Python type annotations for all function parameters and return types to improve code clarity and IDE support."},
        ]
        collection.add(
            documents=[s["text"] for s in standards],
            ids=[s["id"] for s in standards]
        )
    
    return collection
    
def retrieve_relevant_standards(code: str, n_results: int = 3):
    collection = get_chroma_collection()
    results = collection.query(
        query_texts=[code],
        n_results=n_results,
        include=["documents", "distances"]
    )
    docs = results["documents"][0]
    distances = results["distances"][0]
    
    # Log relevance
    for doc, dist in zip(docs, distances):
        print(f"Relevance score (lower=better): {dist:.4f} | {doc[:60]}...")
    
    return "\n".join([f"- {doc}" for doc in docs])