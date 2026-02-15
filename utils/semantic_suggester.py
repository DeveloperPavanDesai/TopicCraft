def calculate_similarity(nlp, topic, text):
    topic_doc = nlp(topic)
    text_doc = nlp(text)
    return round(topic_doc.similarity(text_doc), 2)

def refine_text(topic, text):

    replacements = {
        "always": "often",
        "completely": "significantly",
        "many advantages": "significant advantages",
        "some problems": "notable challenges"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    improved_intro = f"{topic} is playing an increasingly important role in modern society. "

    refined_text = improved_intro + text

    return refined_text
