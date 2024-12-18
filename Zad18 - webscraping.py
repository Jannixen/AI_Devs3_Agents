# Author: Joanna Koła
# Date: 2024-11-26
# Version: 1.0
# Description: Script is working in loop looking for the answers to the provided questions.
#              GPT 4 model is supposed to look for the answer to the question in the scrapped text or
#              the url to the page where it can be

import json
import requests
from dotenv import load_dotenv
import os
from functions import ask_llm
import html2text

# Load the .env file
load_dotenv()
agent_key = os.getenv('AGENT_KEY')
api_key = os.getenv('OPENAI_API_KEY')


verify_url = "https://centrala.ag3nts.org/report"
questions_url = f"https://centrala.ag3nts.org/data/{agent_key}/softo.json"
content_url = "https://softo.ag3nts.org"

questions = requests.get(questions_url, verify=False)
questions = questions.text


def scrap_web(url):
    response = requests.get(url, verify=False)
    html_object = html2text.HTML2Text()
    html_object.ignore_links = False  # Optional: Ignore links, can be set to False if you want to keep them
    html_content = html_object.handle(response.text)  # Process HTML and convert to text
    return html_content


def build_prompt(questions, response_format, prompt_rule, conversation_history):
    main_prompt = f"Twoim zadaniem jest przeszukanie podanego w zapytaniu tekstu HTML i odpowiedź na pytania {questions}. " \
                  f"Jeśli w załączonym HTML nie ma odpowiedzi na pytania przeanalizuj treść strony i poszukaj linków do " \
                  f"następnych stron które mogą zawierać odpowiedzi. W takim przypadku zwróć link do strony która może " \
                  f"zawierać odpowiedź \n {response_format} \n {prompt_rule} \n <conversation_history> {conversation_history}" \
                  f"</conversation_history>"
    return main_prompt


response_format = """
<response_format>
{
"thinking": [your related thinking process]
"answer": [odpowiedz na pytanie]
"url" : [url gdzie szukać dalej, zostaw puste w momencie kiedy wszystkie odpowiedzi uzupełnione]
}
</response_format>
"""

prompt_rule = """
<prompt_rules>
- Zawsze analizuj całą konwersację aby uzyskać odpowiedź 
- Nie zwracaj żadnych dodatkowych treści, tylko opisany JSON format
- W każdym kroku filtruj tylko zawartość tekstu która może ci pomóc
- Uzupełniaj thinking jako swój proces myślowy który prowadził do otrzymania answer lub url
</prompt_rules>
"""

conversation_history = ""

root_url = "https://softo.ag3nts.org/"
new_url = root_url
html_content = scrap_web(content_url)

while new_url != "":
    main_prompt = build_prompt(questions, response_format, prompt_rule, conversation_history)
    ai_response = ask_llm(html_content, model_name='gpt-4o', system_message=main_prompt, tokens_n=500, temp=0.2)
    ai_response = ai_response.strip('```json').strip('```')
    print(ai_response)
    ai_response = json.loads(ai_response)
    conversation_history += f"USER: {html_content}"
    conversation_history += f"AI: {str(ai_response)}"
    if root_url not in ai_response['url']:
        new_url = content_url + ai_response['url']
    html_content = scrap_web(new_url)

"""
odpowiedzi = ["01": "kontakt@softoai.whatever",
"02": `https://banan.ag3nts.org/`,
"03": 'Firma otrzymała certyfikaty ISO 9001 oraz ISO/IEC 27001'
]
"""
