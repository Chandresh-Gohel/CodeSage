from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from standards import retrieve_relevant_standards
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite-preview",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

template = """
You are an experienced code reviewer.

**Retrieved Coding Standards:**
{standards}

**Review the function on clarity, correctness, efficiency, security, maintainability, and Python best practices.**

Function code:
{code}
"""

prompt = ChatPromptTemplate.from_template(template)

# LCEL pipe operator — modern LangChain
chain = prompt | llm | StrOutputParser()

def review_code_diff(diff_text: str) -> str:
    relevant_standards = retrieve_relevant_standards(diff_text)
    response = chain.invoke({"standards": relevant_standards, "code": diff_text})
    return response.strip()