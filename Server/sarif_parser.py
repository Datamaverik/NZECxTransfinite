import json


# Function to parse SARIF result file and display vulnerability details
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
    except KeyError as e:
        print(f"Error parsing SARIF file: Missing key {e}")
