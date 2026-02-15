# TopicCraft

**TopicCraft** is an AI-powered writing assistant that analyzes your drafts with NLP (spaCy), suggests refinements, and surfaces style and bias insights—all in a simple Streamlit app.

## Features

- **Topic relevance** — Enter an optional topic; get a similarity score and topic-focused refinements for your draft.
- **Refined text** — Automatically suggests improved wording (e.g. softening absolutes, clearer phrasing) and can prepend a topic-focused intro.
- **Basic statistics** — Sentence count, word count, average sentence length, and vocabulary richness.
- **Named entities** — Extracts people, orgs, places, dates, etc. (spaCy `en_core_web_sm`).
- **Key phrases** — Noun chunks for quick scan of main concepts.
- **POS distribution** — Part-of-speech breakdown (nouns, verbs, adjectives, etc.).
- **Passive voice** — Highlights sentences in passive voice for optional rewrites.
- **Bias words** — Flags terms like “always”, “never”, “completely”, “disaster”, “amazing” to support more neutral tone.

## How This Project Helps

**For writers**

- Suggests missing or underdeveloped subtopics via key phrases and entities.
- Improves clarity with refined text and readability stats.
- Reduces repetition via vocabulary richness and phrase views.
- Detects biased or overly emotional tone with bias-word checks.

**For businesses**

- Standardizes content tone and encourages neutral wording.
- Ensures more consistent, professional communication.
- Supports SEO and structure via entity and phrase extraction.

## Tech Stack

- **Python 3** — Core runtime.
- **Streamlit** — Web UI.
- **spaCy** — NLP pipeline (`en_core_web_sm`).
- **pandas** — Tables and charts.
- **scikit-learn** — Used by spaCy for similarity (if applicable).

## Project Structure

```
TopicCraft/
├── app.py                 # Streamlit entry point
├── requirements.txt       # Python dependencies
├── README.md
├── utils/
│   ├── nlp_loader.py      # Load spaCy model
│   ├── text_statistics.py # Sentence/word/vocab stats
│   ├── entity_extractor.py# Named entities & noun chunks
│   ├── style_analyzer.py  # POS distribution, passive voice
│   ├── semantic_suggester.py # Topic similarity, text refinement
│   └── bias_detector.py   # Bias word detection
├── assets/
│   └── logo/              # App logo
├── notebooks/             # Research & prototyping
└── .streamlit/            # Streamlit config
```

## Installation

1. **Clone and enter the repo**

   ```bash
   git clone <repo-url>
   cd TopicCraft
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download the spaCy language model**

   ```bash
   python -m spacy download en_core_web_sm
   ```

## Run the App

From the project root:

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`).

## Usage

1. **Topic** (optional) — e.g. “Climate change and renewable energy”. Used for relevance scoring and refined intro.
2. **Draft** — Paste your text in the text area.
3. **Analyze** — Click to get refined text, stats, entities, key phrases, POS distribution, passive-voice sentences, and bias words.

Results appear in expandable sections; you can use the refined text as a starting point for edits.