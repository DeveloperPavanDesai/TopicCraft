import html
import streamlit as st
import pandas as pd

from utils.nlp_loader import load_nlp_model
from utils.text_statistics import basic_statistics
from utils.entity_extractor import extract_entities, extract_noun_chunks
from utils.style_analyzer import pos_distribution, detect_passive_voice
from utils.semantic_suggester import calculate_similarity, refine_text
from utils.bias_detector import detect_bias

st.set_page_config(
    page_title="TopicCraft - AI Writing Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .hero {
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid rgba(49, 51, 63, 0.2);
    }
    .hero h1 {
        font-size: 2.25rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.25rem;
    }
    .hero .subtitle {
        color: var(--text-muted, #73818c);
        font-size: 1rem;
        font-weight: 400;
    }
    .stMetric {
        background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        padding: 1rem 1.25rem;
        border-radius: 10px;
        border: 1px solid rgba(49, 51, 63, 0.15);
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }
    h2, h3 {
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        margin-top: 1.5rem !important;
    }
    .refined-block {
        background: rgba(49, 51, 63, 0.08);
        padding: 1.25rem 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
        line-height: 1.6;
    }
    .score-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.25rem;
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
        color: white;
    }
    .dataframe thead tr th {
        background: rgba(49, 51, 63, 0.12) !important;
        font-weight: 600 !important;
    }
    .streamlit-expanderHeader {
        font-weight: 600;
    }
    div[data-testid="column"] {
        padding: 0 0.5rem;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(30,41,59,0.03) 0%, transparent 100%);
    }
    [data-testid="stSidebar"] .stMarkdown {
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### How to use")
    st.markdown("""
    1. Enter a **topic** (optional) to check relevance and get topic-focused refinements.
    2. Paste your **draft** in the text area.
    3. Click **Analyze** to get refined text, stats, entities, and style checks.
    """)
    st.markdown("---")
    st.markdown("**TopicCraft** helps you improve drafts with NLP: topic relevance, key phrases, passive voice, and bias checks.")

st.markdown('<div class="hero"><h1>TopicCraft</h1><p class="subtitle">AI Writing Assistant — refine drafts and analyze style</p></div>', unsafe_allow_html=True)

col_topic, _ = st.columns([2, 1])
with col_topic:
    topic = st.text_input("Topic", placeholder="e.g. Climate change and renewable energy", label_visibility="collapsed")
st.text_area("Draft", value="", height=280, placeholder="Paste your draft here…", label_visibility="collapsed", key="draft")

analyze_clicked = st.button("Analyze", type="primary", use_container_width=False)

if analyze_clicked:
    text = st.session_state.get("draft", "")
    if (text or "").strip() == "":
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing…"):
            nlp = load_nlp_model()
            doc = nlp(text)

        if topic and topic.strip():
            score = calculate_similarity(nlp, topic, text)
            st.markdown("#### Topic relevance")
            st.markdown(f'<span class="score-badge">{score:.2f}</span>', unsafe_allow_html=True)
            st.markdown("")

        st.markdown("#### Refined text")
        refined = refine_text(topic, text)
        refined_safe = html.escape(refined).replace("\n", "<br>")
        st.markdown(f'<div class="refined-block">{refined_safe}</div>', unsafe_allow_html=True)

        st.markdown("#### Basic statistics")
        stats = basic_statistics(doc)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Sentences", stats["sentences"])
        with c2:
            st.metric("Words", stats["words"])
        with c3:
            st.metric("Avg sentence length", f'{stats["avg_sentence_length"]}')
        with c4:
            st.metric("Vocab richness", f'{stats["vocab_richness"]}')
        stats_df = pd.DataFrame(list(stats.items()), columns=["Metric", "Value"]).set_index("Metric")
        st.bar_chart(stats_df)

        st.markdown("---")

        with st.expander("Named entities", expanded=True):
            entities = extract_entities(doc)
            if entities:
                ent_df = pd.DataFrame(entities, columns=["Entity", "Type"])
                ent_counts = ent_df["Type"].value_counts()
                col_t, col_c = st.columns([1, 1])
                with col_t:
                    st.dataframe(ent_df, use_container_width=True, hide_index=True)
                with col_c:
                    st.bar_chart(pd.DataFrame({"Count": ent_counts}))
            else:
                st.info("No named entities detected.")

        with st.expander("Key phrases"):
            noun_chunks = extract_noun_chunks(doc)
            if noun_chunks:
                chunk_series = pd.Series(noun_chunks).value_counts()
                chunk_df = pd.DataFrame({"Phrase": chunk_series.index, "Count": chunk_series.values})
                st.dataframe(chunk_df, use_container_width=True, hide_index=True)
                st.bar_chart(pd.DataFrame({"Count": chunk_series.head(15)}))
            else:
                st.info("No key phrases extracted.")

        with st.expander("POS distribution"):
            pos_dist = pos_distribution(doc)
            pos_df = pd.DataFrame(list(pos_dist.items()), columns=["POS", "Count"]).set_index("POS").sort_values("Count", ascending=False)
            st.bar_chart(pos_df)

        with st.expander("Passive voice sentences"):
            passive = detect_passive_voice(doc)
            if passive:
                for i, sent in enumerate(passive, 1):
                    st.write(f"{i}. {sent}")
            else:
                st.success("No passive voice sentences found.")

        with st.expander("Bias words"):
            bias = detect_bias(doc)
            if bias:
                st.write(" ".join([f"`{w}`" for w in bias]))
            else:
                st.success("No bias words detected.")