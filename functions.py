# Author: Joanna Koła
# Date: 2024-12-09
# Version: 3.0
# Description: File contains functions used while doing the course tasks


import base64
import requests
import openai
from dotenv import load_dotenv
import os
from typing import Any, Dict, Optional

# Load the .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')


def post_json(data_url: str, json_content: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    try:
        response = requests.post(data_url, json=json_content, verify=False)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()  # Directly return the JSON response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def ask_llm(question: str, model_name: str = "gpt-4o-mini", system_message: str = "Give me short and specific answer",
            tokens_n: int = 500, temp: float = 0.0):
    openai.api_key = api_key
    client = openai.Client(api_key=openai.api_key)
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": question}
        ],
        max_tokens=tokens_n,
        temperature=temp
    )
    return response.choices[0].message.content.strip()


def transcribe_image(image_file_path: str) -> str:
    encoded_image = base64.b64encode(open(image_file_path, 'rb').read()).decode('utf-8')
    image_url = f"data:image/png;base64,{encoded_image}"
    client = openai.Client(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Get text from image"},
            {"role": "user",
             "content": "Please read the text from the image and return it as a string, without adding any additional "
                        "text or comments"},
            {"role": "user", "content": image_url}
        ],
        max_tokens=1000,
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


def transcribe_audio(audio_file):
    client = openai.Client(api_key=api_key)
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language="pl"  # Specify the language of the audio, change if necessary
    )
    return transcript


def generate_image_from_text(text_description):
    client = openai.Client(api_key=api_key)
    url_image = client.images.generate(model="dall-e-3", response_format="url", size="1024x1024",
                                       prompt=f"Generate an image corresponding to description: {text_description}. "
                                              f"Refrain from adding any additional objects, not mentioned in the "
                                              f"description")

    return url_image
