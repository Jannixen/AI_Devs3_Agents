# Author: Joanna Koła
# Date: 2024-11-25
# Version: 1.0
# Description: Script is preparing training data for custom OpenAI model made for classifying arrays of numbers as correct or incorrect


import json
import random
from typing import List


def read_and_process_file(file_path: str) -> List[List[str]]:
    """Reads a text file and processes its content into a list of lists."""
    with open(file_path, 'r') as f:
        return [line.split(',') for line in f.read().splitlines()]


def write_jsonl_file(file_path: str, data: List[List[str]], text_name: str) -> None:
    """Writes data to a JSONL file in the specified format."""
    with open(file_path, 'a') as file:
        for sub_array in data:
            json_obj = {
                "messages": [
                    {"role": "system", "content": "Określ poprawność ciągu danych"},
                    {"role": "user", "content": f"{sub_array}"},
                    {"role": "assistant", "content": f"{text_name}"}
                ]
            }
            file.write(json.dumps(json_obj) + '\n')


def prepare_text_file_for_finetuning(text_name: str, file_type: str) -> None:
    """Prepares a text file for fine-tuning by converting its content to JSONL format."""
    correct_data = read_and_process_file(f'{text_name}.txt')
    write_jsonl_file(f'{file_type}.jsonl', correct_data, text_name)


def read_lines_from_file(file_path: str) -> List[str]:
    """Reads lines from a file and returns them as a list."""
    with open(file_path, 'r') as file:
        return file.readlines()


def write_lines_to_file(file_path: str, lines: List[str]) -> None:
    """Writes a list of lines to a file."""
    with open(file_path, 'w') as file:
        file.writelines(lines)


def mix_and_split_jsonl_file(input_file: str, train_file: str, validation_file: str, train_ratio: float = 0.7) -> None:
    """Shuffles and splits a JSONL file into training and validation sets."""
    # Read the lines from the JSONL file
    lines = read_lines_from_file(input_file)

    # Shuffle the lines
    random.shuffle(lines)

    # Calculate the split index
    split_index = int(len(lines) * train_ratio)

    # Split the lines into train and validation sets
    train_lines = lines[:split_index]
    validation_lines = lines[split_index:]

    # Write the train lines to the train JSONL file
    write_lines_to_file(train_file, train_lines)

    # Write the validation lines to the validation JSONL file
    write_lines_to_file(validation_file, validation_lines)


prepare_text_file_for_finetuning('correct', 'train')
prepare_text_file_for_finetuning('incorrect', 'train')

mix_and_split_jsonl_file('train.jsonl', 'train_mixed.jsonl', 'validation.jsonl')
