import openai
import json
import dotenv
# from dotenv import load_dotenv
import os

dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Set up your OpenAI API key
openai.api_key = OPENAI_API_KEY


def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use 'gpt-4' or 'gpt-3.5-turbo' based on your access level
            messages=[
                {
                    "role": "system",
                    "content": "act as the world's greatest static code analyzer for all major programming languages. I will give you a code snippet, and you will identify the language and analyze it for vulnerabilities. Give the output in a format: filename, vulnerabilities detected as a numbered list, and proposed fixes as a separate numbered list.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=2000,  # Adjust max tokens for response length
            temperature=0.7,  # Adjust temperature for response randomness
        )

        # Extract the code (corrected output) from the response
        corrected_code = response.choices[0].message["content"]

        # Print the full JSON response for debugging or insight
        print("Complete JSON Response:")
        print(json.dumps(response, indent=2))  # Pretty-print the JSON response

        # Convert the specific part of the response containing the code into JSON format
        json_response = json.dumps(corrected_code, indent=2)

        return json_response
    except Exception as e:
        return str(e)


# Example JSON prompt
prompt_text = {
    "prompt": """iimport os import urllib
from flask import Flask, request
from django.db import connection, models
from django.db.models.expressions import RawSQL

app = Flask(__name__)

@app.route("/code-execution")
def code_execution():
    code1 = request.args.get("code1")
    exec("setname('%s')" % code1)
    return a

@app.route("/open-redirect")
def open_redirect():
    redirect_loc = request.args.get('redirect')
    return redirect(redirect_loc)


@app.route("/sqli/<username>")
def show_user(username):
    with connection.cursor() as cursor:
      cursor.execute("SELECT * FROM users WHERE username = '%s'" % username)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)

"""
}

# Convert the prompt to a JSON string and send it to the API
response_json = chat_with_gpt(prompt_text["prompt"])

# Print the response received in JSON format
print("Response received from ChatGPT API:\n", response_json)

