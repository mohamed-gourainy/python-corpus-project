# Author.py

class Author:
    """
    Représente un auteur du corpus.
    """
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = {}   # id_doc → Document

    def add(self, doc_id, document):
        """Ajoute un document à la production de l'auteur."""
        self.production[doc_id] = document
        self.ndoc += 1

    def taille_moyenne_docs(self):
        """Retourne la taille moyenne (en caractères) des documents de l'auteur."""
        if self.ndoc == 0:
            return 0
        total = sum(len(doc.texte) for doc in self.production.values())
        return total / self.ndoc

    def __str__(self):
        return f"Auteur : {self.name} — {self.ndoc} document(s)"
