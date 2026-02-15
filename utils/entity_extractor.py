def extract_entities(doc):
    return [(ent.text, ent.label_) for ent in doc.ents]

def extract_noun_chunks(doc):
    return [chunk.text for chunk in doc.noun_chunks]