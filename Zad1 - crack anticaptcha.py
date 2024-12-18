# Author: Joanna Koła
# Date: 2024-11-04
# Version: 1.0
# Description: This script scraps content of web page in html,
#              gets question from captcha, generates answer for it with OpenAI model and then passes verification

import requests
from bs4 import BeautifulSoup
from functions import ask_llm

data_url = "https://xyz.ag3nts.org/"

response = requests.get(data_url, verify=False)
html_content = response.text

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find the element with the ID 'human-question' on html page and get the question text
human_question = soup.find(id="human-question").get_text(strip=True)

# Ask LLM to answer the captcha question
answer = ask_llm(human_question, system_message="Zwróć wyłącznie krótką, precyzyjną odpowiedź np. miejsce, rok",
                 tokens_n=5)

# send LLM answer to site
site_response = requests.post(data_url, data={"username": "tester", "password": '574e112a', "answer": str(answer)},
                              verify=False)

print(site_response.status_code)
print(site_response.text)
