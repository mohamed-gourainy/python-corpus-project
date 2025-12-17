# DocumentFactory.py

from Document import Document, RedditDocument, ArxivDocument


class DocumentFactory:
    """
    Patron d'usine (Factory Pattern) pour créer des documents.
    """

    @staticmethod
    def create(doc_type, titre, auteur, date, url, texte,
               nb_comments=0, coauthors=None):
        doc_type = doc_type.lower()

        if doc_type == "reddit":
            return RedditDocument(
                titre=titre,
                auteur=auteur,
                date=date,
                url=url,
                texte=texte,
                nb_comments=nb_comments
            )
        elif doc_type == "arxiv":
            return ArxivDocument(
                titre=titre,
                auteur_principal=auteur,
                date=date,
                url=url,
                texte=texte,
                coauthors=coauthors
            )
        else:
            # type générique par défaut
            return Document(
                titre=titre,
                auteur=auteur,
                date=date,
                url=url,
                texte=texte,
                doc_type="generic"
            )
