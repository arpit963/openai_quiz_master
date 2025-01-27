import json
import requests
import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# Define model and system prompt
def get_question(user_input):
    model = "gpt-3.5-turbo"
    system_prompt = "You are a quiz master. Creating the one liner quizzes with some options is your proficiency."
    message = f"Study the following topics properly: {user_input}. Now generate UNIQUE and entertaining 4 quiz questions in JSON format key is 'quiz' with question, 3 options and ONE correct answer. Each question should be concise, ensuring easy to understand words."
    print("Message : ", message)
    # Prepare the data for the API request
    data = {'model': model,
            'messages': [{'role': 'system', 'content': system_prompt},{'role': 'user', 'content': message}],
            'temperature': 0.2,
            'max_tokens': 1000,
            'top_p': 1,
            'frequency_penalty': 0,
            'response_format': {'type': "json_object"}}

    # Convert to JSON string
    data_json = json.dumps(data)
    # key = os.environ["OPENAI_SECRET_KEY"]

    load_dotenv(Path("/home/decode/Documents/Django_Project/.env"))
    # OpenAI.api_key = str(os.getenv("OPENAI_MAIN_KEY"))
    OpenAI.api_key = str(os.getenv("OPENAI_NEW_KEY"))
    print("API KEY : ", OpenAI.api_key)

    # Set up the headers for the API request
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '+OpenAI.api_key}

    # Define the URL for the OpenAI API
    url = 'https://api.openai.com/v1/chat/completions'

    # Send the POST request
    response = requests.post(url, headers=headers, data=data_json)

    # Check for errors
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
    else:
        # Parse and return the response
        results = response.json()
        question_content = results["choices"][0]["message"]
        question_info = question_content["content"]
        json_object = json.loads(question_info)
        return json_object
