import codeql_scan as cds
import final_route_gpt as frg
import json
import subprocess
import sys
import pathlib
import shutil


def read_file_content(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"File {file_path} not found."
    except Exception as e:
        return f"Error reading {file_path}: {str(e)}"


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


def load_vuln_str(vulns):
    def rmprefix(text, prefix):
        if text.startswith(prefix):
            return text[len(prefix) :]
        return text.strip()

    def rmsuffix(text, suffix):
        if text.endswith(suffix):
            return text[: -len(suffix)]
        return text.strip()

    vulns = rmprefix(vulns, "Answer:").strip()
    vulns = rmprefix(vulns, "```json").strip()
    vulns = rmprefix(vulns, "```").strip()
    vulns = rmsuffix(vulns, "```").strip()

    return json.loads(vulns)


def evaluate_repo(github_link):

    response = []

    repo_name = clone_repo(github_link)
    base_path = pathlib.Path.cwd() / repo_name
    assert base_path.exists(), f"Repo {repo_name} not found."

    data = json.loads(cds.main(github_link, repo_name).strip())

    file_paths = [item["file_path"] for item in data]
    messages = [item["message"] for item in data]

    for path in file_paths:
        file = read_file_content(base_path / path)
        x = file + "\n" + "message: " + messages[file_paths.index(path)]
        print("x: ", x)
        print("file: ", file)

        response.append(frg.analyze_code_vulnerabilities(x))

    shutil.rmtree(repo_name)
    response = [load_vuln_str(vuln) for vuln in response]
    return response


def evalate_snippets(snippet):
    frg.analyze_code_vulnerabilities(snippet)



if __name__ == "__main__":
    response = evaluate_repo("https://github.com/Arush-Pimpalkar/vun_codes")

    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(response)
    print(type(response))
    # collect final json for frontend from frg.analyze_code_vulnerabilities()
