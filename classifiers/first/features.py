FEATURES = [
    "one_word_emp",
    "five_word_emb",
    "seventeen_word_emb",
    "five_word_context_emb",
    "seventeen_word_context_emb",
]


def get_config(text, ind):
    config = {
        "one_word_emp": text[ind],
        "five_word_emb": " ".join(text[max(0, ind - 2):min(len(text), ind + 3)]),
        "seventeen_word_emb": " ".join(text[max(0, ind - 8):min(len(text), ind + 9)]),
        "five_word_context_emb": " ".join(text[max(0, ind - 2):ind] + ['<UNK>'] + text[ind + 1:min(len(text), ind + 3)]),
        "seventeen_word_context_emb": " ".join(text[max(0, ind - 8):ind] + ['<UNK>'] + text[ind + 1:min(len(text), ind + 9)]),
    }
    return {key: value for key, value in config.items() if key in FEATURES}
