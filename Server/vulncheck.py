# -*- coding: utf-8 -*-
"""Untitled27.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nXFm9azWs_ybJcQu8rdAMThqRD7LNvWT
"""

import openai
import json
import pandas as pd
import os
from sentence_transformers import SentenceTransformer, util
import dotenv
dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


# Function to call GPT-4 API
def analyze_code_vulnerabilities(user_query):
      # Define your GPT-4 prompt with the user code dynamically inserted
      dataset = [{
          "code" : """
      import pickle

      # Vulnerable deserialization code
      def load_user_data(serialized_data):
          return pickle.loads(serialized_data)

      # Simulate receiving malicious serialized data
      serialized_data = <untrusted user input>
      load_user_data(serialized_data)
      """,
          "vulnerability": "This code uses `pickle.loads` to deserialize untrusted user input. Python's `pickle` module is inherently insecure as it allows execution of arbitrary code during deserialization. This can lead to remote code execution if an attacker sends a malicious serialized payload, potentially compromising the system.",

          "fix" : """
      import json

      # Secure deserialization using JSON
      def load_user_data(serialized_data):
          try:
              return json.loads(serialized_data)
          except json.JSONDecodeError:
              raise ValueError("Invalid data format")

      # Simulate receiving safe serialized data
      serialized_data = '{"username": "user1", "email": "user1@example.com"}'
      load_user_data(serialized_data)
      """
      },
      {
          "code" : """
      # Vulnerable code with hardcoded secret key
      def connect_to_service():
          api_key = "my_secret_api_key_12345"  # Hardcoded API key
          print(f"Connecting to service with API key: {api_key}")

      connect_to_service()
      """,
          "vulnerability": "This code hardcodes an API key directly into the source code. If the code is shared or uploaded to a public repository, the API key could be exposed, potentially allowing unauthorized access to external services and systems. Hardcoded secrets are a common security risk, especially in version control systems.",

          "fix" : """
      import os

      # Secure method using environment variable for the secret key
      def connect_to_service():
          api_key = os.getenv('API_KEY')  # Load API key from environment variable
          if api_key is None:
              raise ValueError("API key not found. Please set the API_KEY environment variable.")
          print(f"Connecting to service with API key: {api_key}")

      # Set the API key as an environment variable before running the script
      connect_to_service()
      """
      },
      {
          "code" : """
      import sqlite3

      # Vulnerable SQL query with user input directly concatenated
      def get_user_data(user_id):
          conn = sqlite3.connect('example.db')
          cursor = conn.cursor()
          query = f"SELECT * FROM users WHERE id = {user_id}"  # Unsafe query
          cursor.execute(query)
          return cursor.fetchall()

      # Simulate an SQL injection attack
      user_id = "1; DROP TABLE users;"  # Malicious input
      get_user_data(user_id)
      """,
          "vulnerability": "This code is vulnerable to SQL injection because user input is directly concatenated into the SQL query string. An attacker can craft malicious inputs to alter the query structure, potentially leading to data leakage, modification, or deletion (e.g., dropping database tables). In this case, the input '1; DROP TABLE users;' could delete the 'users' table.",

          "fix" : """
      import sqlite3

      # Secure SQL query using parameterized statements
      def get_user_data(user_id):
          conn = sqlite3.connect('example.db')
          cursor = conn.cursor()
          query = "SELECT * FROM users WHERE id = ?"  # Use parameterized query
          cursor.execute(query, (user_id,))
          return cursor.fetchall()

      # Safe input, preventing SQL injection
      user_id = "1"
      get_user_data(user_id)
      """
      },
      {
          "code" : """
      import os

      # Vulnerable code allowing directory traversal
      def read_file(filename):
          base_dir = "/var/www/files/"
          file_path = os.path.join(base_dir, filename)  # Insecure file path concatenation
          with open(file_path, 'r') as file:
              return file.read()

      # Simulate directory traversal attack
      filename = "../../etc/passwd"  # Malicious input trying to access sensitive system file
      print(read_file(filename))
      """,
          "vulnerability": "This code is vulnerable to a directory traversal attack because it directly concatenates user input to the file path without validation. An attacker can manipulate the file path (e.g., '../../etc/passwd') to access sensitive files outside the intended directory, potentially compromising system security.",

          "fix" : """
      import os

      # Secure file reading with path validation
      def read_file(filename):
          base_dir = "/var/www/files/"
          full_path = os.path.abspath(os.path.join(base_dir, filename))  # Get absolute path
          if not full_path.startswith(os.path.abspath(base_dir)):  # Ensure the path is within the base directory
              raise ValueError("Access denied: Invalid file path")

          with open(full_path, 'r') as file:
              return file.read()

      # Safe input, preventing directory traversal
      filename = "example.txt"
      print(read_file(filename))
      """
      }]

      df = pd.DataFrame(dataset, columns = ['code','vulnerability','fix'])
      from sentence_transformers import SentenceTransformer, util
      # Load the pre-trained model
      model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

      # Create embeddings for the 'code' column in the dataset
      codes = df['code'].tolist()  # Extract 'code' column as a list
      dataset_embeddings = model.encode(codes, convert_to_tensor=True)

      query_embedding = model.encode(user_query, convert_to_tensor=True)

      # Perform similarity search
      top_k = 3  # Hyperparameter
      cosine_scores = util.pytorch_cos_sim(query_embedding, dataset_embeddings)

      # Get the top-k matches
      top_k_values, top_k_indices = cosine_scores.topk(k=top_k, dim=-1)
      top_k_indices = top_k_indices.tolist()[0]


      # Function to create the prompt
      def create_prompt(dataset, top_k_indices):
          prompt = """
          You are a brilliant software security expert.
          You will be provided with a few examples and a code, you have to answer like the given examples.
          If it contains any CWE security vulnerabilities, explain the vulnerability.
          If the code does not contain any vulnerabilities, return an empty JSON.
          If the code has the vulnerability, write a repaired secure version of the
          code that preserves its exact functionality.
          Format your response an array of vulnerability JSON objects with each
          JSON object having "code" as the key
          for vulnerability status, "vulnerability" to explain the vulnerability,
          and "fix" for the fixed code snippet.
          If there are multiple vulnerabilities just return an array of
          JSON following a format having code, vulnerability, fix keys for each vulnerability and fix
          Think about the answer step by step, and only answer with JSON.\n

          Example for multiple vulnerability
          code:
          from fastapi import FastAPI
          import base64
          import pickle

          app = FastAPI()
          glbl_state = None

          @app.get("/api/load")
          def load_data(data: str):
            global glbl_state
            binary = base64.b64decode(data)
            glbl_state = pickle.loads(binary)
            return {"success" : True}

          @app.get("/sqli/")
          def show_user(username: str):
              with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = '%s'" % username)

          Answer:
          [{
              "vulnerability": {explains vulenrability},
              "code": {gives the code with the vulnerability},
              "fix": {the fixed code with no vurnerabilities}
          }]
          """

          for idx in top_k_indices:
              code_snippet = df.iloc[idx]["code"]
              vulnerability = df.iloc[idx]["vulnerability"]
              fix = df.iloc[idx]["fix"]
              prompt += f"code: {code_snippet}\n"
              prompt += f'Answer: {{"vulnerability": "{vulnerability}", "code": "{code_snippet}", "fix": "{fix}"}}\n\n'

          prompt += "Analyze ONLY the code given below. The given examples are just references. Analyze snippets only from the below code:\n"
          prompt += "code: ```$USER_CODE$```\n"
          prompt += "Answer: "

          return prompt


      # Create the prompt with the top-k examples
      final_prompt = create_prompt(df, top_k_indices)
      #print(final_prompt)
      prompt = final_prompt.replace("$USER_CODE$", user_query)
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
      
      return response.choices[0].message["content"]

def check_vuln(code):
    vulns = analyze_code_vulnerabilities(code)

    def rmprefix(text, prefix):
        if text.startswith(prefix):
            return text[len(prefix):]
        return text.strip()
    
    def rmsuffix(text, suffix):
        if text.endswith(suffix):
            return text[:-len(suffix)]
        return text.strip()
    
    vulns = rmprefix(vulns, "Answer:").strip()
    vulns = rmprefix(vulns, "```json").strip()
    vulns = rmprefix(vulns, "```").strip()
    vulns = rmsuffix(vulns, "```").strip()

    return json.loads(vulns)

# Example of user input handling and API call
# Example user query
user_query = """<?php
function sumOfNumbersInFile($filePath) {
    if (!file_exists($filePath) || !is_readable($filePath)) {
        return "Error: File does not exist or is not readable.";
    }


    $fileContent = file_get_contents($filePath);


    preg_match_all('/-?\d+/', $fileContent, $matches);


    $numbers = array_map('intval', $matches[0]);
    $sum = array_sum($numbers);

    return $sum;
}

// Example usage:
$filePath = 'numbers.txt'; // Replace with the path to your file
$result = sumOfNumbersInFile($filePath);
echo "The sum of numbers in the file is: " . $result;
?>
"""

print(repr(user_query))

if __name__ == "__main__":
    # Analyze the code vulnerabilities
    #print(check_vuln(user_query))
    pass
