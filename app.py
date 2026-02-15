import html
import os
import streamlit as st
import pandas as pd

from utils.nlp_loader import load_nlp_model
from utils.text_statistics import basic_statistics
from utils.entity_extractor import extract_entities, extract_noun_chunks
from utils.style_analyzer import pos_distribution, detect_passive_voice
from utils.semantic_suggester import calculate_similarity, refine_text
from utils.bias_detector import detect_bias

# Favicon: prefer .ico in assets, fallback to logo PNG
_page_icon = None
if os.path.isfile("assets/favicon.ico"):
    _page_icon = "assets/favicon.ico"
elif os.path.isfile("assets/logo/TopicCraft.png"):
    _page_icon = "assets/logo/TopicCraft.png"

st.set_page_config(
    page_title="TopicCraft - AI Writing Assistant",
    page_icon=_page_icon,
    layout="wide",
    initial_sidebar_state="expanded",
)

# White theme + tuned layout
st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 900px;
        margin: 0 auto;
        background-color: #ffffff;
    }
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stSidebar"] [data-testid="block-container"] {
        padding-top: 0 !important;
    }
    [data-testid="stSidebar"] .stMarkdown { font-size: 0.9rem; color: #475569; }
    /* Hero: centered, balanced */
    .hero-wrap {
        text-align: center;
        margin-bottom: 2.5rem;
        padding-bottom: 2rem;
        border-bottom: 1px solid #e2e8f0;
    }
    .hero-wrap h1 {
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin: 0 0 0.25rem 0;
        color: #1e293b;
    }
    .hero-wrap .subtitle {
        color: #64748b;
        font-size: 0.95rem;
        font-weight: 400;
        margin: 0;
    }
    .input-section { margin-top: 0.5rem; }
    /* Metric cards */
    .stMetric {
        background: #f8fafc;
        padding: 1rem 1.25rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    [data-testid="stMetricValue"] { font-size: 1.5rem !important; font-weight: 600 !important; color: #1e293b !important; }
    [data-testid="stMetricLabel"] { color: #64748b !important; }
    /* Section titles in results */
    .result-section { margin-top: 2rem; }
    h2, h3 {
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        margin-top: 1.75rem !important;
        margin-bottom: 0.75rem !important;
        color: #1e293b !important;
        font-size: 1.15rem !important;
    }
    /* Refined text block */
    .refined-block {
        background: #f8fafc;
        padding: 1.25rem 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #f59e0b;
        margin: 0.5rem 0 1rem 0;
        line-height: 1.65;
        color: #334155;
        font-size: 0.95rem;
    }
    .score-badge {
        display: inline-block;
        padding: 0.4rem 0.9rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.1rem;
        background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
        color: white;
    }
    .dataframe thead tr th {
        background: #f1f5f9 !important;
        font-weight: 600 !important;
        color: #1e293b !important;
        border-color: #e2e8f0 !important;
    }
    .dataframe tbody tr td { border-color: #e2e8f0 !important; }
    .streamlit-expanderHeader { font-weight: 600; color: #1e293b; }
    div[data-testid="column"] { padding: 0 0.5rem; }
    /* Inputs */
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {
        background-color: #fafafa !important;
        color: #1e293b !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 0.6rem 0.85rem !important;
        font-size: 0.95rem !important;
    }
    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stTextArea"] textarea::placeholder { color: #94a3b8 !important; }
    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.2) !important;
    }
    /* Analyze button: more prominent */
    .stButton > button[kind="primary"] {
        padding: 0.6rem 1.75rem !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    _logo_path = "assets/logo/TopicCraft.png"
    if os.path.isfile(_logo_path):
        _c1, _c2, _c3 = st.columns([1, 2, 1])
        with _c2:
            st.image(_logo_path, width=220)
    st.markdown("### How to use")
    st.markdown("""
    1. Enter a **topic** (optional) to check relevance and get topic-focused refinements.
    2. Paste your **draft** in the text area.
    3. Click **Analyze** to get refined text, stats, entities, and style checks.
    """)
    st.markdown("---")
    st.markdown("**TopicCraft** helps you improve drafts with NLP: topic relevance, key phrases, passive voice, and bias checks.")

# Hero: centered title (logo is in sidebar)
_, col_center, _ = st.columns([1, 2, 1])
with col_center:
    st.markdown(
        '<div class="hero-wrap">'
        '<h1>TopicCraft</h1>'
        '<p class="subtitle">AI Writing Assistant — refine drafts and analyze style</p>'
        '</div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="input-section"></div>', unsafe_allow_html=True)
topic = st.text_input("Topic", placeholder="e.g. Climate change and renewable energy", label_visibility="collapsed")
st.text_area("Draft", value="", height=260, placeholder="Paste your draft here…", label_visibility="collapsed", key="draft")
st.markdown("<br>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([1, 1, 1])
with btn_col:
    analyze_clicked = st.button("Analyze", type="primary", use_container_width=True)

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