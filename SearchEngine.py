import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SearchEngine:
    """
    TD7 — Moteur de recherche sur un corpus :
    - Construction d'une matrice TF-IDF (sparse) sur les documents
    - Recherche par similarité cosinus entre la requête et les documents
    - Retour des top-N résultats dans un DataFrame
    """

    def __init__(self, corpus, text_getter=None, preprocessor=None, stop_words="english"):
        """
        :param corpus: instance de Corpus (ton projet)
        :param text_getter: fonction(doc) -> str (par défaut doc.texte)
        :param preprocessor: fonction(str) -> str (par défaut None)
        :param stop_words: stop-words pour TfidfVectorizer (ex: "english", None, ou liste)
        """
        self.corpus = corpus
        self.text_getter = text_getter or (lambda d: getattr(d, "texte", ""))
        self.preprocessor = preprocessor
        self.stop_words = stop_words

        self.vectorizer = None
        self.doc_matrix = None  # sparse TF-IDF matrix
        self.doc_ids = []
        self._built = False

    def build(self):
        """
        Construit le vocabulaire + matrice TF-IDF docs×termes.
        À appeler une fois après avoir chargé le corpus.
        """
        self.doc_ids = list(self.corpus.id2doc.keys())
        texts = []
        for doc_id in self.doc_ids:
            doc = self.corpus.id2doc[doc_id]
            t = self.text_getter(doc) or ""
            if self.preprocessor:
                t = self.preprocessor(t)
            texts.append(t)

        # Matrice sparse
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words=self.stop_words,
        )
        self.doc_matrix = self.vectorizer.fit_transform(texts)
        self._built = True
        return self

    def search(self, query, n=10):
        """
        :param query: requête utilisateur (string)
        :param n: nombre de résultats
        :return: DataFrame trié par score décroissant
        """
        if not self._built:
            self.build()

        q = query or ""
        if self.preprocessor:
            q = self.preprocessor(q)

        q_vec = self.vectorizer.transform([q])
        sims = cosine_similarity(q_vec, self.doc_matrix).ravel()

        top_idx = np.argsort(sims)[::-1][:n]
        rows = []
        for idx in top_idx:
            score = float(sims[idx])
            doc_id = self.doc_ids[idx]
            doc = self.corpus.id2doc[doc_id]

            texte = getattr(doc, "texte", "") or ""
            extrait = (texte[:200] + "...") if len(texte) > 200 else texte

            rows.append({
                "score": round(score, 6),
                "id": doc_id,
                "titre": getattr(doc, "titre", ""),
                "auteur": getattr(doc, "auteur", ""),
                "date": getattr(doc, "date", ""),
                "type": doc.getType() if hasattr(doc, "getType") else getattr(doc, "type", ""),
                "url": getattr(doc, "url", ""),
                "extrait": extrait,
            })

        return pd.DataFrame(rows).sort_values("score", ascending=False).reset_index(drop=True)
