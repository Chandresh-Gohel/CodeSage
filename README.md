# CodeSage: AI-Powered Code Review System

CodeSage is an AI-powered code review system that leverages Google’s Gemini API to provide detailed code reviews for Python functions. It automatically extracts code diffs from Git repositories, reviews each function, and offers feedback on various aspects of the code, including clarity, correctness, efficiency, security, maintainability, and Python best practices.

## Features

* **Git Diff Extraction**: Automatically fetches code changes from a Git repository.
* **Function Extraction**: Extracts added or modified functions from the code diff.
* **Code Review**: Uses AI to review each function based on several criteria (clarity, correctness, efficiency, etc.).
* **Review Storage**: Saves the review results for each function in a text file.

## Installation

### Prerequisites

* Python 3.x
* Google Cloud account (for accessing the Gemini API)
* GitHub repository access
* `git` command line tool

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/CodeSage.git
   cd CodeSage
   ```

2. Install required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the Google API key:

   * Create a `.env` file in the root of the project with the following content:

   ```bash
   GOOGLE_API_KEY=your-google-api-key
   ```

4. Ensure that `git` is installed and available in your PATH.

## Usage

1. **Start the review process**:

   The code will automatically extract the most recent changes made to the repository and identify added or modified functions. The extracted function code is then passed to Google's Gemini API for review.

2. **Review Output**:

   The review for each function is saved in a text file. The file contains detailed feedback on the function, addressing aspects like clarity, correctness, efficiency, security, and best practices.

### Example

To start the code review process, call the function that triggers the review:

```python
# src/main.py

repo_url = "https://github.com/yourusername/yourrepo.git"
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
    print("This is Review" + review)
    file_path = os.path.join("reviews", f"function_{i}_{change_type}.txt")
    with open(file_path, 'w') as f:
        f.write(review)
    print(f"Review saved to {file_path}")
```

In this example:

* The function fetches the diff from the specified repository.
* It extracts the added or modified functions.
* For each function, a review is generated and saved in a file in the `reviews/` directory.

### Notes

* The review process currently only analyzes the most recent commit.
* If the most recent commit doesn't contain any function changes, no reviews will be generated.
* The review files are saved in the `reviews/` directory.

## Project Structure

```
CodeSage/
├── src/
│   ├── git_diff.py   # Logic for fetching Git diffs and extracting functions
│   ├── llm_review.py # Code review functionality using Google's Gemini API
│   ├── main.py       # Main script to trigger the review process
│   └── utils.py      # Helper functions for file operations and other utilities
├── .env              # Environment variables (Google API key)
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

## License

This project is licensed under the MIT License.