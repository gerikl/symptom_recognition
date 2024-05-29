from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    Doc,
    NamesExtractor,
    DatesExtractor,
    MoneyExtractor,
    NewsSyntaxParser,
    NewsNERTagger,
)

from data_processing import DataLoader, calculate_iou

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)



dataloader = DataLoader()
raw_text = dataloader.get_text(dataloader.get_files(1)[0])
text = list(raw_text.values())[0]
doc = Doc(text)
print(doc)



