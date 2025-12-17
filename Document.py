# Document.py

class Document:
    """
    Classe mère de tous les documents du corpus.
    """
    def __init__(self, titre, auteur, date, url, texte, doc_type="generic"):
        self.titre = titre
        self.auteur = auteur
        self.date = date      # ici string simple, ex: "2023"
        self.url = url
        self.texte = texte
        self.type = doc_type  # "reddit", "arxiv", ...

    def afficher(self):
        print("Titre  :", self.titre)
        print("Auteur :", self.auteur)
        print("Date   :", self.date)
        print("URL    :", self.url)
        print("Texte  :", self.texte[:150], "...")

    def getType(self):
        """Retourne le type de document (reddit, arxiv, etc.)."""
        return self.type

    def __str__(self):
        return f"{self.titre} ({self.date})"


class RedditDocument(Document):
    """
    Document spécifique à Reddit.
    Ajoute par exemple le nombre de commentaires.
    """
    def __init__(self, titre, auteur, date, url, texte, nb_comments=0):
        super().__init__(titre, auteur, date, url, texte, doc_type="reddit")
        self.nb_comments = nb_comments

    # accesseurs / mutateurs simples
    def get_nb_comments(self):
        return self.nb_comments

    def set_nb_comments(self, n):
        self.nb_comments = n

    def getType(self):
        return "reddit"

    def __str__(self):
        return f"[Reddit] {self.titre} ({self.date}) - {self.nb_comments} commentaires"


class ArxivDocument(Document):
    """
    Document spécifique à Arxiv.
    Ajoute la gestion des co-auteurs (liste de noms).
    """
    def __init__(self, titre, auteur_principal, date, url, texte, coauthors=None):
        super().__init__(titre, auteur_principal, date, url, texte, doc_type="arxiv")
        if coauthors is None:
            coauthors = []
        self.coauthors = coauthors  # liste de str

    def get_coauthors(self):
        return self.coauthors

    def add_coauthor(self, name):
        self.coauthors.append(name)

    def getType(self):
        return "arxiv"

    def __str__(self):
        if self.coauthors:
            others = ", ".join(self.coauthors)
            return f"[Arxiv] {self.titre} ({self.date}) - {self.auteur} et {others}"
        else:
            return f"[Arxiv] {self.titre} ({self.date}) - {self.auteur}"
