from langchain_community.embeddings import HuggingFaceEmbeddings


def get_model(name: str):
    if name == 'first':
        model_name = "ai-forever/sbert_large_nlu_ru"
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': False}
        hf = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
        return hf
    return
