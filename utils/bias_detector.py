def detect_bias(doc):
    bias_words = ["always", "never", "completely", "disaster", "amazing"]
    
    found = [
        token.text for token in doc
        if token.text.lower() in bias_words
    ]
    
    return found