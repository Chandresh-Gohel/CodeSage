# src/llm_review.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")
def review_code_diff(diff_text: str) -> str:
    prompt = """
    You are an experienced code reviewer. Your task is to thoroughly review the function provided below. 
    Please evaluate the function on the following criteria:

    1. **Clarity**:
    - Is the code easy to understand?
    - Are the variable names clear and descriptive?
    - Does the function include helpful comments or docstrings?

    2. **Correctness**:
    - Does the function perform the intended task correctly?
    - Are there edge cases that need to be handled (e.g., null values, type errors, empty inputs)?
    - Is the function well-tested or does it have test cases provided?

    3. **Efficiency**:
    - Is the code optimized for performance?
    - Are there any unnecessary calculations or data structures that could be simplified?
    - Could the function be more efficient in terms of time or space complexity?

    4. **Security**:
    - Does the function introduce any security risks (e.g., SQL injection, unsafe handling of user input)?
    - Is input validation properly implemented to prevent malicious input?

    5. **Maintainability**:
    - Is the code easy to maintain and extend?
    - Does the function follow the DRY (Don't Repeat Yourself) principle?
    - Could the function be refactored to improve readability or reduce complexity?

    6. **Python Best Practices**:
    - Does the code follow **PEP 8** guidelines for Python code style?
    - Are there any Pythonic improvements (e.g., list comprehensions, context managers)?
    - Are standard libraries used effectively where applicable?

    **Review Format**:
    - **Summary**: Briefly describe what the function does.
    - **Improvements**: Suggest specific improvements for each of the above criteria.
    - **Possible Issues**: Highlight any potential bugs, security issues, or performance bottlenecks.
    - **Code Suggestions**: If possible, provide an improved version of the code with suggested changes.

    Function code:
    """

    {diff_text}
    response = model.generate_content(prompt)
    return response.text.strip()