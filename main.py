# main_td6.py

from Corpus import Corpus
from DocumentFactory import DocumentFactory


def main():
    # ===== 1) Récupérer l'unique instance du corpus (Singleton) =====
    corpus = Corpus.get_instance("Corpus TD6 final")
    factory = DocumentFactory()

    # ===== 2) Créer quelques documents de test =====

    # Reddit
    doc1 = factory.create(
        doc_type="reddit",
        titre="Climate change is real",
        auteur="RedditUser123",
        date="2023",
        url="https://reddit.com/fake1",
        texte="This is a discussion about climate change on Reddit. Climate change is a serious issue.",
        nb_comments=42
    )

    # Arxiv avec co-auteurs
    doc2 = factory.create(
        doc_type="arxiv",
        titre="Deep Learning for Climate Models",
        auteur="Dr. Smith",
        date="2024",
        url="https://arxiv.org/fake2",
        texte="This paper explores deep learning models applied to climate data. "
              "We show that neural networks can help predict climate patterns.",
        coauthors=["Dr. Johnson", "Dr. Lee"]
    )

    # Document générique
    doc3 = factory.create(
        doc_type="generic",
        titre="Random blog post",
        auteur="Anonymous",
        date="2022",
        url="http://example.com/random",
        texte="Just a random text about environment, weather, and daily life. Nothing very scientific."
    )

    # Ajout au corpus
    corpus.add_document(doc1)
    corpus.add_document(doc2)
    corpus.add_document(doc3)

    # ===== 3) Affichage général du corpus =====
    print("=== CORPUS ===")
    print(corpus)

    # ===== 4) Tri par date =====
    print("\n=== Documents triés par date ===")
    corpus.afficher_par_date(n=10)

    # ===== 5) Tri par titre =====
    print("\n=== Documents triés par titre ===")
    corpus.afficher_par_titre(n=10)

    # ===== 6) Afficher les sources / types =====
    print("\n=== Documents avec leur type/source ===")
    corpus.afficher_sources()

    # ===== 7) Statistiques pour un auteur =====
    print("\n=== Statistiques pour l'auteur 'Dr. Smith' ===")
    corpus.stats_auteur("Dr. Smith")

    # ===== 8) Sauvegarde du corpus =====
    print("\n=== Sauvegarde du corpus dans 'corpus_td6.tsv' ===")
    corpus.save("corpus_td6.tsv")

    # ===== 9) Test de SEARCH (TD6) =====
    print("\n=== SEARCH sur le mot 'climate' ===")
    matches = corpus.search("climate")
    print("Nombre d'occurrences trouvées :", len(matches))
    print("Exemples de matches :", matches[:5])

    # ===== 10) Test du CONCORDANCIER (TD6) =====
    print("\n=== CONCORDE sur 'climate' (contexte=25) ===")
    concorde_df = corpus.concorde("climate", contexte=25)
    print(concorde_df)

    # ===== 11) Test des STATS (TD6) =====
    print("\n=== STATS (top 10 mots) ===")
    freq_df = corpus.stats(n=10)
    print("\nDataFrame des fréquences :")
    print(freq_df)


if __name__ == "__main__":
    main()
