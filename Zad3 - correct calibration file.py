# Author: Joanna Koła
# Date: 2024-11-06
# Version: 1.0
# Description: This script downloads the long question and answer
#              text with mistakes. The aim is to correct them using AI model but the content is too long for one prompt

import requests
import json
import re
from dotenv import load_dotenv
import os

from functions import ask_llm

# Load the .env file
load_dotenv()
agent_key = os.getenv('AGENT_KEY')

data_url = "https://centrala.ag3nts.org/data/7eabd929-6873-4a9d-8315-d25502254148/json.txt"
verify_url = "https://centrala.ag3nts.org/report"

response = requests.get(data_url, verify=False)
data = json.loads(response.text)
text_data = str(data["test-data"])


def find_segments(input_string):
    return re.findall(r'\{.*?\}', input_string)


def replace_segments_with_placeholders(input_string, placeholder='###SEGMENT###'):
    return re.sub(r'\{.*?\}', placeholder, input_string)


def split_non_segment_parts(temp_string, placeholder='###SEGMENT###'):
    return temp_string.split(placeholder)


def calculate_length_per_part(non_segment_parts, parts):
    total_length = sum(len(part) for part in non_segment_parts)
    return total_length // parts


def create_divided_parts(non_segment_parts, segments, length_per_part):
    divided_parts = []
    current_part = ''
    current_length = 0

    for i, part in enumerate(non_segment_parts):
        current_part += part
        current_length += len(part)

        if i < len(segments):
            current_part += segments[i]

        if current_length >= length_per_part or i == len(non_segment_parts) - 1:
            divided_parts.append(current_part)
            current_part = ''
            current_length = 0

    return divided_parts


def adjust_parts(divided_parts, parts):
    while len(divided_parts) < parts:
        if len(divided_parts) > 1:
            divided_parts[-2] += divided_parts.pop()
        else:
            break
    return divided_parts


def divide_string(input_string, parts=5):
    segments = find_segments(input_string)
    temp_string = replace_segments_with_placeholders(input_string)
    non_segment_parts = split_non_segment_parts(temp_string)
    length_per_part = calculate_length_per_part(non_segment_parts, parts)
    divided_parts = create_divided_parts(non_segment_parts, segments, length_per_part)
    return adjust_parts(divided_parts, parts)


parts = divide_string(text_data, 10)
corrected_parts = ""

for part in parts:
    corrected_part = ask_llm(part, model_name="gpt-4o-mini",
                             system_message="I will send you the 5 parts of the text with questions and answers."
                                            " The questions are indicated by {'question', 'q'}, answers by "
                                            "{'answer', 'a'}. Correct every question, even non-arythmetic ones."
                                            "When there is an error in answer then correct it and return me  only the "
                                            "corrected text",
                             tokens_n=4000)
    corrected_parts += corrected_part

# Create a dictionary with the required keys and values
data = {
    "apikey": f"{agent_key}",
    "description": "This is simple calibration data used for testing purposes. Do not use it in production environment!",
    "copyright": "Copyright (C) 2238 by BanAN Technologies Inc.",
    "test-data": f"{corrected_parts}"
}

response = requests.post(verify_url, json={
    "task": "JSON",
    "apikey": agent_key,
    "answer": data
}, verify=False)

print(response.text)
