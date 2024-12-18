# Author: Joanna Koła
# Date: 2024-11-14
# Version: 1.0
# Description: This script generates the new image using DALL-E model based on text description

import json
import requests
from dotenv import load_dotenv
import os
from functions import generate_image_from_text

# Load the .env file
load_dotenv()
agent_key = os.getenv('AGENT_KEY')
api_key = os.getenv('OPENAI_API_KEY')

data_url = f"https://centrala.ag3nts.org/data/{agent_key}/robotid.json"
verify_url = "https://centrala.ag3nts.org/report"

response = requests.get(data_url, verify=False)
data = json.loads(response.text)

description = data['description']

dalle_response = generate_image_from_text(description)
url_image = dalle_response.data[0].url

response = requests.post(verify_url, json={
    "task": "robotid",
    "apikey": agent_key,
    "answer": url_image}, verify=False)
