from itertools import accumulate
import pandas as pd
import numpy as np
import tqdm
import time

from features import get_config, FEATURES


class DataLoader():
    def __init__(self, texts_filename, symptoms_se_filename):
        self._texts_filename = texts_filename
        self._symptoms_se_filename = symptoms_se_filename
        self.texts = self._get_texts()
        self.symptoms_se = self._get_symptoms_se()

    def _get_texts(self):
        with open(self._texts_filename, "r") as file:
            texts = file.readlines()
        return texts
    
    def _get_symptoms_se(self):
        with open(self._symptoms_se_filename, "r") as file:
            symptoms_se = file.readlines()
        return symptoms_se


def do_target(text_id, texts, sympts, bioes=False):
    text = texts[text_id].split(" ")
    sympt = sympts[text_id].split(";$&(")[1:]
    sympt[-1] = sympt[-1][:-1]
    lengthes = map(lambda x: len(x) + 1, text)
    indexes = list(accumulate(lengthes))
    indexes.insert(0, 0)
    indexes.append(indexes[-1] + 10)
    word_ind_map = {index: i for i, index in enumerate(indexes)}
    targets = [0] * len(text)
    for symptom in sympt:
        start_end = symptom[:-1].split(", ")
        start, end = int(start_end[0]), int(start_end[1])
        cur_word = word_ind_map[start]
        rrr = 1
        while indexes[cur_word] + 1 < end:
            targets[cur_word] = rrr
            cur_word += 1
            rrr = 2
    
    if not bioes:
        return targets

    # BIOES-метод
    bioes_targets = []
    for i in range(len(targets)):
        prev = 0 if i == 0 else targets[i - 1]
        next = 0 if i == len(targets) - 1 else targets[i + 1]
        if targets[i] == 0:
            bioes_targets.append(0)  # Out
        elif targets[i] == 1:
            if next == 2:
                bioes_targets.append(1)  # Begin
            else:
                bioes_targets.append(4)  # Single
        else:
            assert prev != 0
            if next == 0:
                bioes_targets.append(3)  # End
            else:
                bioes_targets.append(2)  # Inside

    return bioes_targets


def do_emb(hf, query):
    return hf.embed_query(query)


def get_union(texts, sympts, hf, use_calculated=False, bioes=False):
    all_data = pd.DataFrame(columns=["target", *FEATURES])
    glob_ind = 0

    if not use_calculated:
        # for text_id in tqdm.tqdm(range(1)):
        for text_id in tqdm.tqdm(range(len(texts))):
            text = texts[text_id].split(" ")
            targets = np.array(do_target(text_id, texts, sympts, bioes))
            for ind in range(len(text)):
                config = get_config(text, ind)
                all_data.loc[glob_ind] = [
                    targets[ind],
                    *[do_emb(hf, config[feature]) for feature in FEATURES],
                ]
                glob_ind += 1
        if bioes:
            all_data.to_csv("classifiers/embeddings/embeddings_bioes.csv", index=False)
        else:
            all_data.to_csv("classifiers/embeddings/embeddings.csv", index=False)
    else:
        if bioes:
            all_data = pd.read_csv("classifiers/embeddings/embeddings_bioes.csv")
        else:
            all_data = pd.read_csv("classifiers/embeddings/embeddings.csv")
        for column in all_data.columns:
            if column != "target":
                all_data[column] = all_data[column].apply(lambda x: np.array(list(map(float, x[1:-1].split(", ")))))
    return pd.concat([
        *[all_data[column].apply(pd.Series) for column in all_data.columns if (column != "target") and (column in FEATURES)],
        all_data[['target']]
    ], axis=1)
