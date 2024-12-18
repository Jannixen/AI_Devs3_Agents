# Author: Joanna Koła
# Date: 2024-11-25
# Version: 1.0
# Description: Script is using created fine-tuned model to classify test arrays

import requests
from dotenv import load_dotenv
import os

from functions import ask_llm

# Load the .env file
load_dotenv()
agent_key = os.getenv('AGENT_KEY')
api_key = os.getenv('OPENAI_API_KEY')
train_model_name = os.getenv("FINETUNED_MODEL_CIAGI")

verify_url = "https://centrala.ag3nts.org/report"

with open('verify.txt', 'r') as f:
    correct_data = f.read().split('\n')
    verify_map = {item.split('=')[0]: item.split('=')[1] for item in correct_data if '=' in item}

correct_ids = []
for array_id, array in verify_map.items():
    response = ask_llm(f"{array}", train_model_name, system_message="Określ poprawność ciągu danych", tokens_n=100)

    if response == 'correct':
        correct_ids.append(array_id)

response = requests.post(verify_url, json={
    "task": "research",
    "apikey": agent_key,
    "answer": correct_ids,
}, verify=False)

print(response.text)
