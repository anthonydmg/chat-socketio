import spacy

nlp = spacy.load("es_core_news_md")

def tokenize_spacy(text):
    doc = nlp(text)
    return [str(token) for token in  doc]