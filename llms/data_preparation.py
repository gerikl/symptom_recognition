from data_processing import DataLoader
import time


DELIMETER = ';$&'


def cook_right_data():
    for filename in [
        'processed_data/sorted_symptoms_name.txt',
        'processed_data/sorted_symptoms_start_end.txt',
        'processed_data/sorted_texts.txt',
        'processed_data/sorted_xPaths.txt',
    ]:
        with open(filename, 'w') as f:
            pass
    
    loader = DataLoader()
    for filename in loader.get_files():
        dct = {}  # xPath: (text, symptoms, symptoms_start_end)
        xPath = ""
        text = ""
        symptoms = ""
        symptoms_start_end = ""
        symptoms = loader.get_symptoms(filename)
        xPath_and_texts = loader.get_text(filename)
        for xPath, text in xPath_and_texts.items():
            if xPath not in dct:
                dct[xPath] = ["", "", ""]
            dct[xPath][0] = text
        for symptom in symptoms:
            xPath = symptom['xPath']
            name = symptom['name']
            start = symptom['start']
            end = symptom['end']
            if xPath not in dct:
                dct[xPath] = ["", "", ""]
            dct[xPath][1] += DELIMETER
            dct[xPath][1] += str(name)
            dct[xPath][2] += DELIMETER
            dct[xPath][2] += str((start, end))
        for xPath, (text, symptoms, symptoms_start_end) in dct.items():
            text = text.replace('\n', ' ').strip().lower()
            symptoms = symptoms.replace('\n', ' ').strip().lower().strip('.')
            xPath = xPath.replace('\n', ' ')
            symptoms_start_end = symptoms_start_end.replace('\n', ' ')
            if xPath != '/ClinicalDocument/component/structuredBody/component[3]/section/text':
                continue
            with open('processed_data/sorted_symptoms_name.txt', 'a') as sorted_symptoms_name:
                sorted_symptoms_name.write(symptoms + '\n')
            with open('processed_data/sorted_symptoms_start_end.txt', 'a') as sorted_symptoms_start_end:
                sorted_symptoms_start_end.write(symptoms_start_end + '\n')
            with open('processed_data/sorted_texts.txt', 'a') as sorted_texts:
                sorted_texts.write(text + '\n')
            with open('processed_data/sorted_xPaths.txt', 'a') as sorted_xPaths:
                sorted_xPaths.write(xPath + '\n')


if __name__ == '__main__':
    # main()
    cook_right_data()
