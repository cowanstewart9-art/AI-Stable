import os
import sys
import json
import google.generativeai as genai
from github import Github

def main():
    gemini_key = os.environ.get("GEMINI_API_KEY")
    github_token = os.environ.get("GITHUB_TOKEN")

    if not gemini_key:
        print("Error: GEMINI_API_KEY not set.")
        sys.exit(1)
    if not github_token:
        print("Error: GITHUB_TOKEN not set.")
        sys.exit(1)

    # Initialize Gemini
    try:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"Error configuring Gemini: {e}")
        sys.exit(1)

    # Initialize GitHub
    try:
        g = Github(github_token)
        repo_name = os.environ.get("GITHUB_REPOSITORY")
        event_path = os.environ.get("GITHUB_EVENT_PATH")

        if not repo_name:
            print("Error: GITHUB_REPOSITORY environment variable missing.")
            sys.exit(1)

        if not event_path:
             # Fallback if running locally for testing purposes, but mostly intended for Actions
            print("Warning: GITHUB_EVENT_PATH not set. Cannot determine PR details.")
            sys.exit(0)

        with open(event_path, 'r') as f:
            event_data = json.load(f)

        pr_number = event_data.get("pull_request", {}).get("number")

        if not pr_number:
            print("Not a pull request event or PR number missing.")
            sys.exit(0)

        repo = g.get_repo(repo_name)
        pr = repo.get_pull(pr_number)

        # Get Diff
        # We iterate over files to get the patch.
        # Note: Large diffs might hit token limits. Truncation might be needed for production use.
        files = pr.get_files()
        diff_text = ""
        for file in files:
            # Skip deleted files or binary files if patch is None
            if file.patch:
                diff_text += f"File: {file.filename}\n"
                diff_text += f"```diff\n{file.patch}\n```\n\n"

        if not diff_text:
            print("No changes found or no patches available.")
            return

        # Prompt Gemini
        prompt = f"""
        You are an expert code reviewer acting as a replacement for GitHub Copilot.
        Please review the following code changes and provide constructive feedback,
        suggestions for improvements, and identify potential bugs or security issues.

        If the code looks good, just say "LGTM".

        Code Changes:
        {diff_text}
        """

        print("Sending diff to Gemini...")
        response = model.generate_content(prompt)
        review_comment = response.text

        # Post comment
        print("Posting comment to GitHub...")
        pr.create_issue_comment(f"## Gemini Code Review\n\n{review_comment}")
        print("Review posted successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
