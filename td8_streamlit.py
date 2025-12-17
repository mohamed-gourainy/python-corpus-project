import streamlit as st
from Corpus import Corpus
from DocumentFactory import DocumentFactory
from SearchEngine import SearchEngine

st.set_page_config(page_title="TD8 - Recherche (TF-IDF)", layout="wide")
st.title("TD8 — Interface interactive de recherche (TF-IDF)")

# Charger corpus
@st.cache_data
def load_corpus():
    corpus = Corpus.get_instance("Corpus TD8 Streamlit")
    if not corpus.id2doc:
        factory = DocumentFactory()
        corpus.load("corpus_td6.tsv", factory)
    return corpus

corpus = load_corpus()

# Construire moteur (TD7)
@st.cache_resource
def build_engine(_corpus):
    engine = SearchEngine(
        _corpus,
        preprocessor=Corpus.nettoyer_texte,
        stop_words="english"
    ).build()
    return engine

engine = build_engine(corpus)

st.sidebar.write(f"Docs: **{corpus.ndoc}**")
st.sidebar.write(f"Auteurs: **{corpus.naut}**")

query = st.text_input("Requête :", value="climate")
topn = st.slider("Top N :", 1, 50, 10)

if st.button("Rechercher"):
    df = engine.search(query, n=topn)
    st.subheader("Résultats (TD7)")
    st.dataframe(df, use_container_width=True)

st.markdown("---")
st.subheader("Concordancier (TD6)")
motif = st.text_input("Motif (regex) :", value="climate")
ctx = st.slider("Contexte :", 10, 100, 30)

if st.button("Afficher concorde"):
    dfc = corpus.concorde(motif, contexte=ctx)
    st.dataframe(dfc.head(50), use_container_width=True)
