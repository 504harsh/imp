import os
import random
import subprocess
from datetime import datetime, timedelta

def get_positive_int(prompt, default=20):
    while True:
        try:
            user_input = input(f"{prompt} (default {default}): ")
            if not user_input.strip():
                return default
            value = int(user_input)
            if value > 0:
                return value
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_repo_path(prompt, default="."):
    while True:
        user_input = input(f"{prompt} (default current directory): ")
        if not user_input.strip():
            return default
        if os.path.isdir(user_input):
            return user_input
        else:
            print("Directory does not exist. Please enter a valid path.")

def get_filename(prompt, default="data.txt"):
    user_input = input(f"{prompt} (default {default}): ")
    if not user_input.strip():
        return default
    return user_input

def random_date_jan1_to_apr25_2025():
    # Start: 2025-01-01 00:00:00
    start = datetime(2025, 1, 1, 0, 0, 0)
    # End inclusive: 2025-04-25 23:59:59
    end = datetime(2025, 4, 25, 23, 59, 59)
    total_seconds = int((end - start).total_seconds())
    offset = random.randint(0, total_seconds)
    return start + timedelta(seconds=offset)

def make_commit(date, repo_path, filename, message="graph-greener!"):
    filepath = os.path.join(repo_path, filename)
    with open(filepath, "a") as f:
        f.write(f"Commit at {date.isoformat()}\n")

    subprocess.run(["git", "add", filename], cwd=repo_path, check=True)

    env = os.environ.copy()
    # ISO 8601 is accepted by Git for author/committer dates
    date_str = date.strftime("%Y-%m-%dT%H:%M:%S")
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str

    subprocess.run(["git", "commit", "-m", message], cwd=repo_path, env=env, check=True)

def main():
    print("="*60)
    print("🌱 graph-greener - GitHub Contribution Commit Generator 🌱")
    print("="*60)
    print("This will create commits dated only between 1 Jan 2025 and 25 Apr 2025.\n")

    num_commits = get_positive_int("How many commits do you want to make", 20)
    repo_path = get_repo_path("Enter the path to your local git repository", ".")
    filename = get_filename("Enter the filename to modify for commits", "data.txt")

    print(f"\nMaking {num_commits} commits in repo: {repo_path}\nModifying file: {filename}\n")

    for i in range(num_commits):
        commit_date = random_date_jan1_to_apr25_2025()
        print(f"[{i+1}/{num_commits}] Committing at {commit_date.strftime('%Y-%m-%d %H:%M:%S')}")
        make_commit(commit_date, repo_path, filename)

    print("\nPushing commits to your remote repository...")
    subprocess.run(["git", "push"], cwd=repo_path, check=True)
    print("✅ Done! Check the Jan 1–Apr 25, 2025 area of your GitHub contribution graph in a few minutes.\n")
    print("Tip: Ensure commits go to the default branch and the Git email matches a verified address on the account.")

if _name_ == "_main_":
    main()
