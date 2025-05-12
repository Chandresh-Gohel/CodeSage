import requests
import os

GITHUB_API = "https://api.github.com"

diffpath = os.path.abspath(os.path.join(os.getcwd(), "..", "CodeSage/diffs/"))

def get_git_diff(repo_url, branch="main"):
    """
    Automatically fetch the diff between the latest commit and the previous one from a GitHub repository.

    :param repo_url: GitHub repository URL, e.g., 'https://github.com/owner/repo'
    :return: The diff as a string
    """
    # Extract user and repo from the URL
    parts = repo_url.rstrip(".git").split("/")[-2:]
    user, repo = parts

    # Get latest commits
    commits_url = f"{GITHUB_API}/repos/{user}/{repo}/commits?sha={branch}&per_page=2"
    response = requests.get(commits_url)
    response.raise_for_status()
    commits = response.json()

    if len(commits) < 2:
        raise Exception("Not enough commits to compute a diff.")

    latest = commits[0]["sha"]
    previous = commits[1]["sha"]

    # Get the diff
    compare_url = f"{GITHUB_API}/repos/{user}/{repo}/compare/{previous}...{latest}"
    compare_response = requests.get(compare_url, headers={"Accept": "application/vnd.github.v3.diff"})
    compare_response.raise_for_status()

    return compare_response.text

def save_raw_diff(diff_text, path="raw_diff.diff"):
    """
    Save the raw diff text to a file.

    :param diff_text: The diff text to save
    :param name: The name of the file to save the diff as
    :return: The file path where the diff is saved
    """
    file_path = os.path.join(diffpath,path)

    with open(file_path, 'w') as f:
        f.write(diff_text)
    print(f"Raw diff saved to {os.path.abspath(file_path)}")