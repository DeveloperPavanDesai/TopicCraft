def basic_statistics(doc):
    sentences = list(doc.sents)
    tokens = [token for token in doc if not token.is_punct]

    num_sentences = len(sentences)
    num_words = len(tokens)
    avg_sentence_length = num_words / num_sentences if num_sentences > 0 else 0

    unique_words = len(set([token.lemma_.lower() for token in tokens]))
    vocab_richness = unique_words / num_words if num_words > 0 else 0

    return {
        "sentences": num_sentences,
        "words": num_words,
        "avg_sentence_length": round(avg_sentence_length, 2),
        "vocab_richness": round(vocab_richness, 2)
    }