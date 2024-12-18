# Author: Joanna Koła
# Date: 2024-11-11
# Version: 1.0
# Description: This script uses Whisper model to transcribe audio file to text
#              and then uses it to obtain answer for a very specific question from GPT-4

import json
import requests
from dotenv import load_dotenv
import os
from functions import transcribe_audio, ask_llm

# Load the .env file
load_dotenv()
agent_key = os.getenv('AGENT_KEY')
api_key = os.getenv('OPENAI_API_KEY')

audio_path = f"../audio/"
transcript_path = f"../audio_text/"
verify_url = "https://centrala.ag3nts.org/report"

# Part 1. Prepare transcript using GPT-4

for file in os.listdir(audio_path):
    with open(audio_path + file, "rb") as audio_file:
        transcript = transcribe_audio(audio_file)
    with open(transcript_path + file[:-4] + '.txt', 'w') as save_file:
        save_file.write(transcript.text)

# Part 2. Answer the question based on the transcription

context = ""

for file in os.listdir(transcript_path):
    with open(transcript_path + file, "r") as transcript:
        text = transcript.read()
        context += text

response = ask_llm(
    "Przeanalizuj dla mnie tekst zwrócony jako context i wywnioskuj na jakiej uczelni i jakim instytucie "
    "wykłada Andrzej Maj, w jakim mieście i na jakiej ulicy. Zwróć odpowiedź w formacie"
    '{"thinking": "<proces myślowy prowadzący do otrzymania odpowiedzi>", "answer": "<nazwa_ulicy>"}'
    , model_name="gpt-4o-mini", system_message=context,
    tokens_n=500, temp=0.2)

response = requests.post(verify_url, json={
    "task": "mp3",
    "apikey": agent_key,
    "answer": json.loads(response)['answer']
}, verify=False)

print(response.text)
