from collections import Counter

def pos_distribution(doc):
    pos_counts = Counter([token.pos_ for token in doc])
    return dict(pos_counts)


def detect_passive_voice(doc):
    passive_sentences = []
    for token in doc:
        if token.dep_ == "nsubjpass":
            passive_sentences.append(token.sent.text)
    return passive_sentences