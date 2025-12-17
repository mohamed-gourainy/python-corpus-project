# Corpus.py

from Document import Document, RedditDocument, ArxivDocument
from Author import Author
import pandas as pd
import re
from collections import Counter


class Corpus:
    """
    Corpus TD4 + TD5 + TD6 :
    - gestion documents
    - auteurs
    - tri
    - save / load
    - Singleton
    - Factory friendly
    - search()
    - concorde()
    - nettoyage texte
    - statistiques TF / DF
    """

    _instance = None  # Singleton

    @classmethod
    def get_instance(cls, nom="Corpus"):
        if cls._instance is None:
            cls._instance = Corpus(nom)
        return cls._instance

    def __init__(self, nom):
        # Évite de réinitialiser si instance déjà créée
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.nom = nom
        self.authors = {}     # nom → Author
        self.id2doc = {}      # id → Document / RedditDocument / ArxivDocument
        self.ndoc = 0
        self.naut = 0

        # Pour TD6 (cache)
        self._full_text = None

        self._initialized = True

    # =====================================================
    # AJOUT DOCUMENTS (TD4 + TD5)
    # =====================================================
    def add_document(self, document):
        doc_id = self.ndoc
        self.id2doc[doc_id] = document

        # Gestion des auteurs
        auteur = document.auteur
        if auteur not in self.authors:
            self.authors[auteur] = Author(auteur)

        self.authors[auteur].add(doc_id, document)

        self.ndoc += 1
        self.naut = len(self.authors)

        # Le corpus change → on invalide le texte concaténé
        self._full_text = None

    # =====================================================
    # TRI (TD4)
    # =====================================================
    def afficher_par_date(self, n=5):
        docs = sorted(self.id2doc.values(), key=lambda d: d.date)[:n]
        for d in docs:
            print(d)

    def afficher_par_titre(self, n=5):
        docs = sorted(self.id2doc.values(), key=lambda d: d.titre)[:n]
        for d in docs:
            print(d)

    def afficher_sources(self):
        for doc_id, doc in self.id2doc.items():
            print(f"id={doc_id} | type={doc.getType()} | {doc}")

    # =====================================================
    # STATS AUTEURS (TD4)
    # =====================================================
    def stats_auteur(self, name):
        if name not in self.authors:
            print("Auteur inconnu :", name)
            return
        aut = self.authors[name]
        print(aut)
        print("Taille moyenne des documents :", aut.taille_moyenne_docs())

    def __repr__(self):
        return f"Corpus '{self.nom}' : {self.ndoc} documents, {self.naut} auteurs"

    # =====================================================
    # SAUVEGARDE / LOAD (TD5)
    # =====================================================
    def save(self, filename):
        rows = []
        for doc_id, doc in self.id2doc.items():
            row = {
                "id": doc_id,
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": doc.date,
                "url": doc.url,
                "texte": doc.texte,
                "type": doc.getType()
            }

            # Champs spécifiques TD5
            if doc.getType() == "reddit":
                row["nb_comments"] = doc.nb_comments
                row["coauthors"] = ""
            elif doc.getType() == "arxiv":
                row["nb_comments"] = 0
                row["coauthors"] = ";".join(doc.coauthors)
            else:
                row["nb_comments"] = 0
                row["coauthors"] = ""

            rows.append(row)

        df = pd.DataFrame(rows)
        df.to_csv(filename, sep="\t", index=False)
        print("[INFO] Corpus sauvegardé dans", filename)

    def load(self, filename, factory):
        df = pd.read_csv(filename, sep="\t")

        for _, row in df.iterrows():
            doc_type = row.get("type", "generic")
            titre = row["titre"]
            auteur = row["auteur"]
            date = row["date"]
            url = row["url"]
            texte = row["texte"]
            nb_comments = row.get("nb_comments", 0)

            coauthors_str = row.get("coauthors", "")
            coauthors = [c for c in coauthors_str.split(";") if c] if isinstance(coauthors_str, str) else []

            doc = factory.create(
                doc_type=doc_type,
                titre=titre,
                auteur=auteur,
                date=date,
                url=url,
                texte=texte,
                nb_comments=nb_comments,
                coauthors=coauthors
            )

            self.add_document(doc)

        print("[INFO] Corpus chargé depuis", filename)

    # =====================================================
    # TD6 – TEXTE CONCATÉNÉ + SEARCH + CONCORDE
    # =====================================================
    def _build_full_text(self):
        """
        Construit une seule fois la grande chaîne concaténée du corpus (TD6).
        """
        if self._full_text is None:
            textes = [doc.texte for doc in self.id2doc.values()]
            self._full_text = " ".join(textes)
        return self._full_text

    def search(self, motif):
        """
        Retourne simplement les occurrences du motif dans le corpus (TD6).
        """
        texte = self._build_full_text()
        pattern = re.compile(motif, re.IGNORECASE)
        return [m.group(0) for m in pattern.finditer(texte)]

    def concorde(self, motif, contexte=30):
        """
        Concordancier TD6 : gauche | motif | droite (DataFrame)
        """
        texte = self._build_full_text()
        pattern = re.compile(motif, re.IGNORECASE)
        lignes = []

        for m in pattern.finditer(texte):
            start, end = m.start(), m.end()
            gauche = texte[max(0, start-contexte):start]
            centre = texte[start:end]
            droite = texte[end:end+contexte]

            lignes.append({
                "gauche": gauche,
                "motif": centre,
                "droite": droite
            })

        return pd.DataFrame(lignes, columns=["gauche", "motif", "droite"])

    # =====================================================
    # TD6 – NETTOYAGE + VOCABULAIRE + TF + DF
    # =====================================================
    @staticmethod
    def nettoyer_texte(texte):
        """
        Nettoyage TD6 : minuscules + suppression ponctuation + chiffres.
        """
        texte = texte.lower()
        texte = texte.replace("\n", " ")
        texte = re.sub(r"[^a-zA-Z]", " ", texte)
        texte = re.sub(r"\s+", " ", texte)
        return texte.strip()

    def stats(self, n=20):
        """
        Vocabulaire + TF + DF (TD6).
        """
        tf = Counter()
        df = Counter()

        for doc in self.id2doc.values():
            propre = self.nettoyer_texte(doc.texte)
            mots = propre.split()

            tf.update(mots)
            df.update(set(mots))

        print(f"Nombre de mots différents : {len(tf)}")

        top = tf.most_common(n)
        lignes = []

        for mot, freq in top:
            lignes.append({
                "mot": mot,
                "tf": freq,
                "df": df[mot]
            })

        df_res = pd.DataFrame(lignes, columns=["mot", "tf", "df"])
        print(df_res)

        return df_res
