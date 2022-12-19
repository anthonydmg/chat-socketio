from fuzzywuzzy import process


def matching_entity(entity, choices_entities):
    return process.extractOne(entity, choices_entities)


print(matching_entity("titulacion", ["retiro total", "reincorporacion", "retiro parcial","reserva de matricula"]))

import spacy
nlp = spacy.load("es_core_news_md")
def tokenize_spacy(text):
    doc = nlp(text)
    return [str(token) for token in  doc]