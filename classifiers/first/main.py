import numpy as np
import pandas as pd
import tqdm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

from langchain_community.embeddings import HuggingFaceEmbeddings

from data_loader import DataLoader, get_union
from sklearn.metrics import f1_score


def get_model():
    model_name = "ai-forever/sbert_large_nlu_ru"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )


def main():
    texts_filename = "classifiers/data/sorted_texts.txt"
    symptoms_se_filename = "classifiers/data/sorted_symptoms_start_end.txt"
    dl = DataLoader(texts_filename, symptoms_se_filename)
    union = get_union(dl.texts, dl.symptoms_se, get_model(), use_calculated=True, bioes=True)

    train, test = train_test_split(union, test_size=0.2, random_state=666)

    X = train.drop(columns=["target"])
    y = train["target"]
    X_test = test.drop(columns=["target"])
    y_test = test["target"]
    
    np.random.seed(42)  # Fix seed for sklearn
    rf_clf = RandomForestClassifier(max_features="log2", random_state=666)

    rf_clf.fit(X, y)
    prediction = rf_clf.predict(X_test)
    
    print(f"random forest accuracyO: {accuracy_score(prediction, y_test)}")
    print(f"random forest accuracy4: {accuracy_score(prediction[y_test == 4], y_test[y_test == 4])}")
    print(f"random forest accuracy3: {accuracy_score(prediction[y_test == 3], y_test[y_test == 3])}")
    print(f"random forest accuracy2: {accuracy_score(prediction[y_test == 2], y_test[y_test == 2])}")
    print(f"random forest accuracy1: {accuracy_score(prediction[y_test == 1], y_test[y_test == 1])}")
    print(f"random forest accuracy0: {accuracy_score(prediction[y_test == 0], y_test[y_test == 0])}")
    f1 = f1_score(prediction, y_test, average='weighted')
    print(f"random forest f1: {f1}")
    
    
    gb_clf = GradientBoostingClassifier(max_features="log2", random_state=666)

    gb_clf.fit(X, y)
    prediction = gb_clf.predict(X_test)
    
    print(f"gradient bstn accuracyO: {accuracy_score(prediction, y_test)}")
    print(f"gradient bstn accuracy4: {accuracy_score(prediction[y_test == 4], y_test[y_test == 4])}")
    print(f"gradient bstn accuracy3: {accuracy_score(prediction[y_test == 3], y_test[y_test == 3])}")
    print(f"gradient bstn accuracy2: {accuracy_score(prediction[y_test == 2], y_test[y_test == 2])}")
    print(f"gradient bstn accuracy1: {accuracy_score(prediction[y_test == 1], y_test[y_test == 1])}")
    print(f"gradient bstn accuracy0: {accuracy_score(prediction[y_test == 0], y_test[y_test == 0])}")
    f1 = f1_score(prediction, y_test, average='weighted')
    print(f"gradient bstn f1: {f1}")
    
    print('='*100)
    print(prediction[y_test == 4])
    
    svc_clf = SVC(random_state=666)
    
    svc_clf.fit(X, y)
    prediction = svc_clf.predict(X_test)
    f1 = f1_score(prediction, y_test, average='weighted')
    print(f"svc clf f1: {f1}")



if __name__ == '__main__':
    main()


