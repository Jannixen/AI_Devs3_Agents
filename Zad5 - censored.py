# Author: Joanna Koła
# Date: 2024-11-08
# Version: 1.0
# Description: This script downloads the long question and answer
#              text with mistakes. The aim is to correct them using AI model but the content is too long for one prompt

import requests
from dotenv import load_dotenv
import os

from functions import ask_llm

# Load the .env file
load_dotenv()
agent_key = os.getenv('AGENT_KEY')

data_url = f"https://centrala.ag3nts.org/data/{agent_key}/cenzura.txt"
verify_url = "https://centrala.ag3nts.org/report"

censored = ask_llm(requests.get(data_url, verify=False).text,
                   system_message="Zamień wszystkie dane wrażliwe zamieniając je słowem CENZURA."
                                  "Zwróć wyłącznie ocenzurowaną treść zapytania",
                   tokens_n=100)

response = requests.post(verify_url, json={
    "task": "CENZURA",
    "apikey": agent_key,
    "answer": censored
}, verify=False)

print(response.text)
