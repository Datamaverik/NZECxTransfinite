import os
import subprocess
import sys
import json
import requests
import re
import shutil
import dotenv

dotenv.load_dotenv()


def fetch_repo_languages(github_url, token):
    pattern = r"https?://(?:www\.)?github\.com/([^/]+)/([^/]+)"

    match = re.match(pattern, github_url)
    if match:
        owner = match.group(1)
        repo = match.group(2)
    else:
        raise SyntaxError("Invalid GitHub URL format.")

    url = f"https://api.github.com/repos/{owner}/{repo}/languages"

    # Set up the request headers (including authentication)
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "Python",
    }

    # Make the request to the GitHub API
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        languages_data = response.json()  # Parse the JSON response
        return list(languages_data.keys())  # Return an array of language names (keys)
    else:
        raise Exception(
            f"Failed to fetch languages. Status code: {response.status_code}. Error message: {response.text}"
        )


# Function to clone GitHub repo
def clone_repo(github_link):
    repo_name = github_link.split("/")[-1].replace(".git", "")
    clone_command = ["git", "clone", github_link]
    try:
        subprocess.run(clone_command, check=True)
        print(f"Repository '{repo_name}' cloned successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to clone repo: {e}")
        sys.exit(1)
    return repo_name


# Function to set up CodeQL database
def setup_codeql(repo_name, lang):
    codeql_command = [
        "codeql/codeql",
        "database",
        "create",
        f"./{repo_name}-db",
        f"--language={lang}",
        "--source-root",
        f"./{repo_name}",
    ]
    try:
        subprocess.run(codeql_command, check=True)
        print(f"CodeQL database created for repository '{repo_name}'.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create CodeQL database: {e}")
        sys.exit(1)


# Function to run CodeQL query and analyze vulnerabilities
def analyze_vulnerabilities(repo_name):
    query_command = [
        "codeql/codeql",
        "database",
        "analyze",
        f"./{repo_name}-db",
        "--format=sarifv2.1.0",
        "--output",
        f"./{repo_name}_results.sarif",
    ]
    try:
        subprocess.run(query_command, check=True)
        print(f"CodeQL analysis completed for repository '{repo_name}'.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to analyze vulnerabilities: {e}")
        sys.exit(1)


# Function to parse SARIF result file
def parse_sarif_results(repo_name):
    results_file = f"./{repo_name}_results.sarif"
    if not os.path.exists(results_file):
        print("No SARIF results file found.")
        return

    print(f"Parsing vulnerabilities from {results_file}...")

    with open(results_file, "r") as file:
        sarif_data = json.load(file)

    # Traverse the SARIF JSON structure to extract file locations and messages
    try:
        runs = sarif_data["runs"]
        for run in runs:
            results = run.get("results", [])
            for result in results:
                message = result["message"]["text"]
                locations = result.get("locations", [])
                for location in locations:
                    physical_location = location["physicalLocation"]
                    file_path = physical_location["artifactLocation"]["uri"]
                    start_line = physical_location["region"]["startLine"]
                    print(
                        f"Vulnerability found in {file_path} at line {start_line}: {message}"
                    )
                    json_obj = {
                        "file_path": file_path,
                        "start_line": start_line,
                        "message": message,
                    }
                    return json_obj
    except KeyError as e:
        print(f"Error parsing SARIF file: Missing key {e}")


def main(github_link, repo_name):
    token = os.getenv("GH_API_TOKEN")
    json_obj = []

    language_arr = [x.lower() for x in fetch_repo_languages(github_link, token)]
    # repo_name = clone_repo(github_link)

    for lang in language_arr:
        setup_codeql(repo_name, lang)
        analyze_vulnerabilities(repo_name)

        result = parse_sarif_results(repo_name)
        if result:  # Only append if result is not None
            json_obj.append(result)

        # Remove the CodeQL database after analysis
        shutil.rmtree(repo_name + "-db")

    # Output the final JSON object list
    x = json.dumps(json_obj, indent=4)
    print(x)
    # shutil.rmtree(repo_name)  ############################
    return x


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <github_repo_link>")
        sys.exit(1)

    github_repo_link = sys.argv[1]
    main(github_repo_link)
