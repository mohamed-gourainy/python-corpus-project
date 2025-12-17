# app.py

import streamlit as st
import pandas as pd

from Corpus import Corpus
from DocumentFactory import DocumentFactory
from SearchEngine import SearchEngine


# ============================
#  Fonctions utilitaires
# ============================

@st.cache_data
def load_corpus():
    """
    Charge le corpus depuis corpus_td6.tsv en utilisant la factory.
    Singleton pour éviter les doublons.
    """
    corpus = Corpus.get_instance("Corpus TD6 (Streamlit)")
    if not corpus.id2doc:
        factory = DocumentFactory()
        corpus.load("corpus_td6.tsv", factory)
    return corpus


def get_top_stats(corpus, n=20):
    """
    Wrapper autour de corpus.stats()
    """
    return corpus.stats(n=n)


@st.cache_resource
def build_search_engine(_corpus):
    """
    TD7 — Moteur TF-IDF + cosinus
    _corpus : underscore pour éviter le hashing Streamlit
    """
    engine = SearchEngine(
        _corpus,
        preprocessor=Corpus.nettoyer_texte,
        stop_words="english"
    ).build()
    return engine


# ============================
#  Interface Streamlit
# ============================

def main():
    st.set_page_config(
        page_title="Analyse de corpus",
        layout="wide"
    )

    st.title("📚 Interface d'analyse de corpus")
    st.markdown(
        "Application unique couvrant **TD6, TD7 et TD8** : "
        "recherche textuelle, concordancier, statistiques et moteur TF-IDF."
    )

    # Chargement du corpus
    corpus = load_corpus()

    # Barre latérale
    st.sidebar.header("Navigation")
    vue = st.sidebar.radio(
        "Choisir une vue :",
        [
            "Aperçu du corpus",
            "Recherche texte (regex)",
            "Concordancier",
            "Statistiques lexicales (TF/DF)",
            "Recherche TF-IDF (TD7/TD8)"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.write(f"📌 Corpus : **{corpus.nom}**")
    st.sidebar.write(f"📄 Documents : **{corpus.ndoc}**")
    st.sidebar.write(f"🧑‍💻 Auteurs : **{corpus.naut}**")

    # ============================
    # Vue 1 : Aperçu du corpus
    # ============================
    if vue == "Aperçu du corpus":
        st.subheader("📄 Aperçu du corpus")

        docs_data = []
        for doc_id, doc in corpus.id2doc.items():
            extrait = doc.texte[:150] + "..." if len(doc.texte) > 150 else doc.texte
            docs_data.append({
                "id": doc_id,
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": doc.date,
                "type": doc.getType(),
                "url": doc.url,
                "extrait": extrait
            })

        st.dataframe(pd.DataFrame(docs_data), use_container_width=True)

        st.markdown("### 🧑‍💻 Auteurs")
        auteurs_data = [
            {
                "auteur": name,
                "nb_docs": aut.ndoc,
                "taille_moyenne": aut.taille_moyenne_docs()
            }
            for name, aut in corpus.authors.items()
        ]
        st.dataframe(pd.DataFrame(auteurs_data), use_container_width=True)

    # ============================
    # Vue 2 : Recherche regex
    # ============================
    elif vue == "Recherche texte (regex)":
        st.subheader("🔍 Recherche textuelle (regex)")

        motif = st.text_input("Motif (regex) :", value="climate")
        max_res = st.slider("Résultats max :", 1, 50, 10)

        if motif:
            matches = corpus.search(motif)
            st.write(f"**Occurrences trouvées : {len(matches)}**")

            for i, m in enumerate(matches[:max_res], start=1):
                st.write(f"{i}. `{m}`")

    # ============================
    # Vue 3 : Concordancier
    # ============================
    elif vue == "Concordancier":
        st.subheader("📏 Concordancier")

        motif = st.text_input("Motif :", value="climate")
        contexte = st.slider("Contexte :", 10, 100, 30)

        if motif:
            df_conc = corpus.concorde(motif, contexte=contexte)
            st.write(f"Lignes : {len(df_conc)}")
            st.dataframe(df_conc, use_container_width=True)

    # ============================
    # Vue 4 : Stats TF / DF
    # ============================
    elif vue == "Statistiques lexicales (TF/DF)":
        st.subheader("📊 Statistiques lexicales (TF / DF)")

        n = st.slider("Top mots :", 5, 50, 20)
        freq_df = get_top_stats(corpus, n=n)

        st.dataframe(freq_df, use_container_width=True)

        if not freq_df.empty:
            st.bar_chart(freq_df.set_index("mot")[["tf"]])

    # ============================
    # Vue 5 : Recherche TF-IDF (TD7 / TD8)
    # ============================
    elif vue == "Recherche TF-IDF (TD7/TD8)":
        st.subheader("🧠 Recherche avancée TF-IDF (TD7)")

        engine = build_search_engine(corpus)

        query = st.text_input("Requête :", value="climate")
        topn = st.slider("Top N :", 1, 50, 10)

        if st.button("Rechercher (TF-IDF)"):
            df_res = engine.search(query, n=topn)
            st.dataframe(df_res, use_container_width=True)

        st.markdown("---")
        st.markdown("### Concordancier (rappel TD6)")
        motif = st.text_input("Motif (regex) :", value="climate", key="td8_motif")
        ctx = st.slider("Contexte :", 10, 100, 30, key="td8_ctx")

        if st.button("Afficher concorde"):
            dfc = corpus.concorde(motif, contexte=ctx)
            st.dataframe(dfc.head(50), use_container_width=True)


if __name__ == "__main__":
    main()
