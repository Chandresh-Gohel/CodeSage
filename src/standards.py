import chromadb
from chromadb.utils import embedding_functions
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

STANDARDS = [
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

def get_chroma_collection():
    """Initialize ChromaDB collection with coding standards."""
    client = chromadb.PersistentClient(path="./chroma_db")
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    collection = client.get_or_create_collection(
        name="coding_standards",
        embedding_function=ef
    )
    if collection.count() == 0:
        collection.add(
            documents=[s["text"] for s in STANDARDS],
            ids=[s["id"] for s in STANDARDS]
        )
    return collection

def get_langchain_vectorstore():
    """Get LangChain Chroma vectorstore for MMR retrieval."""
    embeddings = SentenceTransformerEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings,
        collection_name="coding_standards"
    )
    return vectorstore

def retrieve_relevant_standards(code: str, n_results: int = 3) -> str:
    """Retrieve relevant standards using MMR for diversity."""
    # Ensure collection is populated
    get_chroma_collection()
    
    vectorstore = get_langchain_vectorstore()
    
    # MMR: fetch_k=10 candidates, pick k=3 most relevant + diverse
    results = vectorstore.max_marginal_relevance_search(
        query=code,
        k=n_results,
        fetch_k=10,
        lambda_mult=0.7  # 0.7 = slightly favour relevance over diversity
    )
    
    print("\n--- MMR Retrieved Standards ---")
    for doc in results:
        print(f"  → {doc.page_content[:70]}...")
    print("-------------------------------\n")
    
    return "\n".join([f"- {doc.page_content}" for doc in results])

def evaluate_recall(test_cases: list) -> float:
    """
    Measure recall@3 — what fraction of expected standards were retrieved.
    
    test_cases format:
    [
        {
            "code": "def foo(): pass",
            "expected_ids": ["docstrings", "pep8"]
        },
        ...
    ]
    """
    collection = get_chroma_collection()
    hits = 0
    total = 0
    
    print("\n--- Recall Evaluation ---")
    for i, case in enumerate(test_cases):
        results = collection.query(
            query_texts=[case["code"]],
            n_results=3
        )
        retrieved_ids = results["ids"][0]
        
        for expected in case["expected_ids"]:
            total += 1
            if expected in retrieved_ids:
                hits += 1
                print(f"  ✓ Case {i+1}: '{expected}' retrieved")
            else:
                print(f"  ✗ Case {i+1}: '{expected}' NOT retrieved — got {retrieved_ids}")
    
    recall = hits / total if total > 0 else 0
    print(f"\nRecall@3: {recall:.2f} ({hits}/{total} expected standards retrieved)")
    print("-------------------------\n")
    return recall

# Test cases for recall evaluation
TEST_CASES = [
    {
        "code": "def add(a, b): return a + b",
        "expected_ids": ["docstrings", "type_hints"]
    },
    {
        "code": "query = 'SELECT * FROM users WHERE id = ' + user_input",
        "expected_ids": ["security_sql", "security_input"]
    },
    {
        "code": "result = []\nfor i in range(len(items)):\n    result.append(items[i]*2)",
        "expected_ids": ["efficiency_loops", "pythonic_comprehension"]
    },
    {
        "code": "try:\n    do_something()\nexcept:\n    pass",
        "expected_ids": ["error_handling"]
    },
    {
        "code": "def process():\n    f = open('file.txt')\n    data = f.read()",
        "expected_ids": ["pythonic_context", "error_handling"]
    },
]

if __name__ == "__main__":
    # Run recall evaluation
    evaluate_recall(TEST_CASES)