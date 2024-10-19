import openai
import dotenv
import os

dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY


# Function to call GPT-4 API
def analyze_code_vulnerabilities(user_code):
    # Define your GPT-4 prompt with the user code dynamically inserted
    prompt = f"""
            You are a brilliant software security expert. 
            You will be provided with a few examples and a python code. 
            If it contains any CWE security vulnerabilities, write Vulnerable. 
            If the code does not contain any vulnerabilities, write Not Vulnerable. 
            If the code has the vulnerability, write a repaired secure version of the
            code that preserves its exact functionality. 
            Format your response as a JSON object with "label" as the key 
            for vulnerability status, "cwe" as the vulnerability found,
            and "fix" for the fixed code snippet. 
            Think about the answer step by step, and only answer with JSON.

            Examples:
            1)
            # Vulnerability: SQL Injection
            # This code is vulnerable to SQL injection as user input is directly concatenated into the query.

            def get_user_data(username):
                query = f"SELECT * FROM users WHERE username = 'username'"
                cursor.execute(query)
                return cursor.fetchall()

            # Corrected Code: Using parameterized queries to prevent SQL injection.

            def get_user_data(username):
                query = "SELECT * FROM users WHERE username = %s"
                cursor.execute(query, (username,))
                return cursor.fetchall()

            2)
            # Vulnerability: Insecure Deserialization
            # This code is vulnerable to insecure deserialization, allowing execution of malicious code.

            import pickle

            def load_user_data(data):
                user_data = pickle.loads(data)
                return user_data

            # Corrected Code: Using safer alternatives like json or explicitly checking data integrity.

            import json

            def load_user_data(data):
                user_data = json.loads(data)
                return user_data

            3)
            # Vulnerability: Hardcoded Secrets
            # This code stores sensitive information, like API keys, directly in the source code.

            def connect_to_api():
                api_key = "my_secret_api_key"
                response = requests.get(f"https://api.example.com/data?key=api_key")
                return response.json()

            # Corrected Code: Store secrets in environment variables instead of hardcoding them.

            import os

            def connect_to_api():
                api_key = os.getenv("API_KEY")
                response = requests.get(f"https://api.example.com/data?key=api_key")
                return response.json()

            python code: {user_code}
            answer:
    """
    # Call the GPT-4 API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "act as the world's greatest static code analyzer for all major programming languages. I will give you a code snippet, and you will identify the language and analyze it for vulnerabilities. Give the output in a format: filename, vulnerabilities detected as a numbered list, and proposed fixes as a separate numbered list.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=1500,  # Adjust based on how detailed you expect the response to be
        n=1,
        stop=None,
        temperature=0,
    )

    # Extracting the response in JSON format
    return response.choices[0].message["content"]


# Example of user input handling and API call
user_code_input = """def vulnerable_function(user_input):
    query = "SELECT * FROM users WHERE username = '" + user_input + "';"
    database.execute(query)
"""

# Analyze the code vulnerabilities
vulnerability_report = analyze_code_vulnerabilities(user_code_input)

# Output the JSON response
print(vulnerability_report)
