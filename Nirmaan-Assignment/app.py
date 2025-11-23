import streamlit as st
import re
import cohere
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import plotly.graph_objects as go

cohere_api_key = "IDlfxdy11paDxht8zQKuLQZkR61dhaPRTwdNzkpF"
co = cohere.Client(cohere_api_key)

keywords = ["name","age","class","hobby","hobbies","interest","goals","goal","family","unique","dream"]
fillers = ["um","uh","hmm","erm","ah","like","you know","so"]

def get_embedding(text):
    resp = co.embed(
        model="embed-multilingual-v3.0",
        texts=[text],
        input_type="search_document"
    )
    return np.array(resp.embeddings[0])

def analyze(transcript: str):
    words = re.findall(r"\w+", transcript)
    tokens = [w.lower() for w in words]
    word_count = len(words)

    keyword_found = {k: bool(re.search(r"\b"+re.escape(k)+r"\b", transcript, flags=re.I)) for k in keywords}
    keyword_ratio = sum(keyword_found.values())/len(keywords)

    salutation = bool(re.search(r"\bhello|hi|good morning|good evening\b", transcript, flags=re.I))
    intro = bool(re.search(r"\bmy name is|myself\b", transcript, flags=re.I))
    core = bool(re.search(r"\bclass|study|family\b", transcript, flags=re.I))
    closing = bool(re.search(r"\bthank you|thanks\b", transcript, flags=re.I))
    flow_score = sum([salutation,intro,core,closing]) / 4

    filler_count = sum(tokens.count(f) for f in fillers)
    filler_rate = (filler_count/word_count)*100 if word_count else 0

    emb_text = get_embedding(transcript)
    emb_rubric = get_embedding("A structured spoken introduction including name, age, class, hobbies, goals and ending well.")
    semantic_sim = float(cosine_similarity([emb_text], [emb_rubric])[0][0])

    content = 0.5*keyword_ratio + 0.25*flow_score + 0.25*semantic_sim
    clarity = 1 - min(filler_rate/12, 1)
    engagement = (semantic_sim + flow_score) / 2

    overall = round((content*0.45 + clarity*0.3 + engagement*0.25)*100,2)

    return overall, keyword_found, keyword_ratio, flow_score, filler_rate, semantic_sim, content, clarity, engagement


st.set_page_config(page_title="Speech Scoring Tool", layout="wide")
st.title("🎤 Nirmaan AI Case Study – Speech Scoring Tool ")

txt = st.text_area("Paste Transcript Here", height=200)

if st.button("Score"):
    overall, k, kr, fs, fr, sim, content, clarity, engagement = analyze(txt)

    st.markdown(f"## ⭐ Overall Score: **{overall} / 100**")

    st.progress(overall/100)

    # Score Chart
    chart = go.Figure(data=[
        go.Bar(
            x=["Content", "Clarity", "Engagement", "Semantic Similarity", "Flow"],
            y=[content*100, clarity*100, engagement*100, sim*100, fs*100],
            text=[content*100, clarity*100, engagement*100, sim*100, fs*100],
            textposition="auto"
        )
    ])

    chart.update_layout(title="📊 Score Breakdown", height=400)
    st.plotly_chart(chart, use_container_width=True)

    # Keywords display
    st.subheader("🔑 Detected Keywords")
    for w, found in k.items():
        if found:
            st.markdown(f"<span style='background:#00cc66; padding:6px; border-radius:8px; margin:4px; display:inline-block;'>{w}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='background:#ff6961; padding:6px; border-radius:8px; margin:4px; display:inline-block;'>{w}</span>", unsafe_allow_html=True)

    # Stats
    st.subheader("📌 Breakdown")
    st.json({
        "Keyword Ratio": kr,
        "Flow Score": fs,
        "Filler Rate (%)": fr,
        "Semantic Similarity": sim,
        "Content Score": content,
        "Clarity Score": clarity,
        "Engagement Score": engagement,
    })
