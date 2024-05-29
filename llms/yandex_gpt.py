import requests
import re
import time

from data_preparation import DELIMETER
from levenshtein_finder import find_closest_in_text
from prompts import BASE_PROMPT, PROMPT_WITH_ONE_SHOT, PROMPT_WITH_TWO_SHOTS, PROMPT_WITH_HALF_SHOT


def get_symptoms_gpt(anamnesis: str, prompt: str = BASE_PROMPT) -> str:
    resp = requests.post(
        url='https://llm.api.cloud.yandex.net/foundationModels/v1/completion',
        headers={
            'Authorization': 'API-KEY <YOUR API_KEY HEAR>',
            'x-folder-id': '<YOUR x-folder-id HERE>'
        },
        json={
            "modelUri": "gpt://b1gqvs6hsa1guvre8m3u/yandexgpt",
            "completionOptions": {
                "stream": False,
                "temperature": 0.15,
                "maxTokens": "1000"
            },
            "messages": [
                {
                    "role": "system",
                    "text": prompt
                },
                {
                    "role": "user",
                    "text": anamnesis
                }
            ]
        }
    )

    answer = resp.json()
    if 'result' not in answer:
        print(answer)
        time.sleep(50)
    return answer['result']['alternatives'][0]['message']['text'].lower().strip()



def cook_symptom(raw_symptoms: str) -> list[str]:
    symptoms = [normalize_gpt_symptom(symptom) for symptom in raw_symptoms.split('\n') if normalize_gpt_symptom(symptom) != '']
    return symptoms


def normalize_gpt_symptom(x: str) -> str:
    symptom = x.replace('*', '').replace('\n', '').lower().strip('-.; ')
    return symptom


def predict():
    with open('processed_data/yandex_gpt_raw_symptoms_sorted.txt', 'w') as symptoms_file:
        pass
    with open('processed_data/sorted_texts.txt', 'r') as file_texts:
        texts = file_texts.readlines()
    raw_symptoms_list = []
    i = 0
    for text in texts:
        raw_symptoms = get_symptoms_gpt(text, prompt=PROMPT_WITH_ONE_SHOT)
        print(raw_symptoms)
        raw_symptoms_list.append(raw_symptoms)
        with open('processed_data/yandex_gpt_raw_symptoms_sorted.txt', 'a') as symptoms_file:
            symptoms_file.write(raw_symptoms + DELIMETER)
        
        time.sleep(0.5)
        i += 1
        # if i == 30:
        #     break



def cook_gpt_answer():
    with open('processed_data/yandex_gpt_symptoms_name.txt', 'w'):
        pass
    with open('processed_data/yandex_gpt_symptoms_start_end.txt', 'w'):
        pass

    with open('processed_data/sorted_texts.txt', 'r') as file_texts:
        texts = file_texts.readlines()
    with open('processed_data/sorted_symptoms_start_end.txt', 'r') as symptoms_start_end_file:
        right_symptoms_list = symptoms_start_end_file.readlines()
    with open('processed_data/yandex_gpt_raw_symptoms_sorted.txt', 'r') as symptoms_file:
        raw_symptoms_list = symptoms_file.read().split(DELIMETER)
        # print(len(texts), len(raw_symptoms_list), len(right_symptoms_list))
        # print('-'*100)
        for text, raw_symptoms, right_symptoms in zip(texts, raw_symptoms_list, right_symptoms_list):
            symptoms_list = cook_symptom(raw_symptoms)
            symptoms_start_end = ""
            symptoms_name = ""
            in_out = 0
            out = 0
            for symptom in symptoms_list:
                in_out += 1
                dist, fixed_symptom = find_closest_in_text(symptom, text)
                if dist > 3:
                    print(symptom)
                    out += 1
                    continue
                start = text.find(fixed_symptom)
                end = start + len(fixed_symptom)
                symptoms_start_end += DELIMETER + str((start, end))
                symptoms_name += DELIMETER + symptom
            with open('processed_data/yandex_gpt_symptoms_name.txt', 'a') as symptoms_name_file:
                symptoms_name_file.write(symptoms_name + '\n')
            with open('processed_data/yandex_gpt_symptoms_start_end.txt', 'a') as symptoms_start_end_file:
                symptoms_start_end_file.write(symptoms_start_end + '\n')
            print(f"Out: {out}, In: {in_out - out}, Right: {len(right_symptoms.split(DELIMETER)) - 1}")



if __name__ == '__main__':
    predict()
    # cook_gpt_answer()
