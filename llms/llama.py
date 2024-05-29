import os
import time

from data_preparation import DELIMETER
from prompts import BASE_PROMPT, PROMPT_WITH_HALF_SHOT

def get_symptoms_llama(anamnesis: str) -> str:
    prompt = f"{PROMPT_WITH_HALF_SHOT} Текст: {anamnesis}. Отвечай на русском"
    os.system(f'echo "{prompt}" | ollama run llama3:8b > llama_output.txt')
    with open('llama_output.txt', 'r') as file:
        return file.read().strip()


def predict():
    with open('processed_data/llama_raw_symptoms_3.txt', 'w') as symptoms_file:
        pass
    with open('processed_data/sorted_texts.txt', 'r') as file_texts:
        texts = file_texts.readlines()
    raw_symptoms_list = []
    i = 0
    for text in texts:
        raw_symptoms = get_symptoms_llama(text)
        print(raw_symptoms)
        raw_symptoms_list.append(raw_symptoms)
        if i == 10:
            break
        i += 1
        
        with open('processed_data/llama_raw_symptoms_3.txt', 'a') as symptoms_file:
            symptoms_file.write(raw_symptoms + DELIMETER)


if __name__ == '__main__':
    predict()
