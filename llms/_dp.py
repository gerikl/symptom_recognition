import os

from data_processing import DataLoader, calculate_iou

loader = DataLoader()

for filename in loader.get_files(2):
    # print(f"Processing {filename}")
    symptoms = loader.get_symptoms(filename)
    text = list(loader.get_text(filename).items())[0][1]
    # print('=='*50)
    # print(text)
    # print('=='*50)
    # print(symptoms)
    # print('=='*50)
    # print()

base_prompt = 'Given the following text, write a summary of the text in 1-2 sentences. \n\n' + text + '\n\nSummary:'
os.system('echo "{base_prompt}" | ollama run llama3 > test.txt')