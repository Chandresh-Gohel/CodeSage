import os
from google import genai
from dotenv import load_dotenv
from  standards import retrieve_relevant_standards

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def review_code_diff(diff_text: str) -> str:
    # RAG: retrieve relevant standards based on the function code
    relevant_standards = retrieve_relevant_standards(diff_text)
    
    prompt = f"""
You are an experienced code reviewer. Review the function below using the retrieved coding standards as context.

**Retrieved Coding Standards (from knowledge base):**
{relevant_standards}

**Review the function on these criteria:**
1. Clarity - variable names, comments, docstrings
2. Correctness - edge cases, type errors, empty inputs
3. Efficiency - time/space complexity, unnecessary operations
4. Security - input validation, injection risks
5. Maintainability - DRY principle, single responsibility
6. Python Best Practices - PEP 8, Pythonic patterns

**Review Format:**
- Summary: what the function does
- Improvements: specific suggestions per criterion
- Possible Issues: bugs, security issues, performance bottlenecks
- Code Suggestions: improved version if applicable

Function code:
{diff_text}
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text.strip()