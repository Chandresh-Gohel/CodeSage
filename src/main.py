# main.py
from git_diff import get_git_diff, save_raw_diff
from extract_functions_from_diff import extract_functions_from_diff
from llm_review import review_code_diff
import os

reviewPATH = os.path.abspath(os.path.join(os.getcwd(), "..", "CodeSage/reviews/"))
repo_url = "YOUR_GITHUB_REPO.git"
branch = "main"

diff_text = get_git_diff(repo_url, branch=branch)
save_raw_diff(diff_text)

functions = extract_functions_from_diff(diff_text)

os.makedirs("reviews", exist_ok=True)
for i, func in enumerate(functions, 1):
    function_code = func["function_code"]
    change_type = func["change_type"]
    print(f"\nReviewing {change_type} function:")
    print(function_code[:100], "...\n")

    review = review_code_diff(function_code)
    file_path = os.path.join(reviewPATH, f"function_{i}_{change_type}.md")
    with open(file_path, 'w') as f:
        f.write(review)
    print(f"Review saved to {file_path}")
