# Author: Joanna Koła
# Date: 2024-11-26
# Version: 1.0
# Description: Script is extracting text from pdf file and then sending it to AI for answers generation


from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv
from functions import ask_llm
import requests

# Load the .env file
load_dotenv()
agent_key = os.getenv('AGENT_KEY')
api_key = os.getenv('OPENAI_API_KEY')
verify_url = "https://centrala.ag3nts.org/report"


def extract_text_pdf(pdf_name: str) -> str:
    reader = PdfReader(pdf_name)
    text = ""

    for page in reader.pages:
        text = page.extract_text()
        text += text

    return text


questions = """
{
    "01": "Do którego roku przeniósł się Rafał",
    "02": "Kto wpadł na pomysł, aby Rafał przeniósł się w czasie?",
    "03": "Gdzie znalazł schronienie Rafał? Nazwij krótko to miejsce",
    "04": "Którego dnia Rafał ma spotkanie z Andrzejem? (format: YYYY-MM-DD)",
    "05": "Gdzie się chce dostać Rafał po spotkaniu z Andrzejem?"
}
"""

full_file_text = extract_text_pdf("notatnik-rafala.pdf")

prompt = f'Na podstawie tekstu {full_file_text} odpowiedz na pytania {questions}. W pytaniu 4 dobrą odpowiedzią nie ' \
         f'jest dokładna data podana w tekście. Podaj odpowiedź w formacie /' \
         f'{"01": "<odpowiedź_1>", "02": "<odpowiedź_2>",..../}'

answers = ask_llm(prompt, model_name="gpt-4o-mini", system_message="Give me specific answer",
                  tokens_n=500, temp=0.2)

response = requests.post(verify_url, json={
    "task": "notes",
    "apikey": agent_key,
    "answer": answers,
}, verify=False)

print(response.text)
