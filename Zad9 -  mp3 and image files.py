# Author: Joanna Koła
# Date: 2024-11-14
# Version: 1.0
# Description: Script is reading various format files (.txt, .mp3, .png) transcribing them using OpenAI models
#              and then performing classification

import os
from dotenv import load_dotenv
import requests

from functions import transcribe_audio, transcribe_image, ask_llm

# Load the .env file
load_dotenv()
agent_key = os.getenv('AGENT_KEY')
api_key = os.getenv('OPENAI_API_KEY')

transcriptions = {}
source_path = "pliki z fabryki/"
verify_url = "https://centrala.ag3nts.org/report"


def transcribe_file(file_name):
    if file_name.endswith(".txt"):
        with open(source_path + file_name, "r") as file:
            transcript = file.read()
    elif file_name.endswith(".mp3"):
        with open(source_path + file_name, "rb") as file:
            transcript = transcribe_audio(file)
    else:
        transcript = transcribe_image(source_path + file_name)
    return transcript


for f in os.listdir(source_path):
    trans = transcribe_file(f)
    transcriptions[f] = trans

response_llm = ask_llm(str(transcriptions), model_name="gpt-4o-mini",
                       system_message="Wyślę ci słownik gdzie wartości to wiadomości które wymagają klasyfikacji ze "
                                      "względu na ich temat. Klasy to [people, hardware, other]. Odeślij mi odpowiedź "
                                      "w formacie {'people': [<lista_plików>], 'hardware': [<lista_plików>]}. "
                                      "Nie zwracaj mi plików należących do klasy other",
                       tokens_n=1000, temp=0.3)

response_verify = requests.post(verify_url, json={
    "task": "kategorie",
    "apikey": agent_key,
    "answer": response_llm.text
}, verify=False)

print(response_verify.text)
