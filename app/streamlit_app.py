import streamlit as st
from dotenv import load_dotenv
load_dotenv()  # load GEMINI_API_KEY/OPENAI_API_KEY from .env into environment for the app
import pandas as pd
from pathlib import Path
import os

from src.retail_insights.data_layer import DataLayer
from src.retail_insights.summarizer import Summarizer
from src.retail_insights.qa_engine import QAEngine


st.set_page_config(page_title="Retail Insights Assistant", layout="wide")

st.title("Retail Insights Assistant — Summarization & Conversational Q&A")

st.markdown("Upload a sales CSV (or use the sample) and choose Summarize or ask a question.")

upload = st.file_uploader("Upload sales CSV", type=["csv", "txt"], help="CSV with at least columns: date, region, product_line, category, units, sales")

use_sample = st.checkbox("Use sample dataset", value=True)

data_layer = DataLayer()

if upload is not None:
    df = pd.read_csv(upload)
    data_layer.register_df(df, table_name='sales')
    st.success("CSV loaded into memory")
elif use_sample:
    sample_path = Path(__file__).parents[1] / "sample_data" / "sample_sales.csv"
    df = pd.read_csv(sample_path)
    data_layer.register_df(df, table_name='sales')
    st.info("Loaded sample dataset")
else:
    st.warning("No dataset loaded yet")

if 'df' in locals():
    with st.expander("View sample data (first 10 rows)"):
        st.dataframe(df.head(10))

st.sidebar.header("Operation")
mode = st.sidebar.selectbox("Mode", ["Summarization", "Conversational Q&A"])

summarizer = Summarizer(data_layer)
qa = QAEngine(data_layer)

if mode == "Summarization":
    st.header("Summarization Mode")
    prompt = st.text_area("Prompt (optional)", value="Summarize overall sales performance and callouts.")
    if st.button("Run Summarization"):
        with st.spinner("Generating summary…"):
            res = summarizer.summarize(prompt)
            st.subheader("Summary")
            st.write(res)

else:
    st.header("Conversational Q&A Mode")
    if 'history' not in st.session_state:
        st.session_state.history = []

    q = st.text_input("Ask a business question about the dataset:")
    if st.button("Ask") and q.strip() != "":
        with st.spinner("Analysing…"):
            ans = qa.ask(q)
            st.session_state.history.append({"q": q, "a": ans})

    if st.session_state.history:
        for item in reversed(st.session_state.history[-10:]):
            st.markdown(f"**Q:** {item['q']}  \n**A:** {item['a']}")
