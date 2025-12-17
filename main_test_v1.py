from Corpus import Corpus
from DocumentFactory import DocumentFactory

def main():
    corpus = Corpus.get_instance("Corpus v1 (TD3-TD5)")
    if not corpus.id2doc:
        factory = DocumentFactory()
        corpus.load("corpus_td6.tsv", factory)  # tu peux charger un TSV existant

    print("=== CORPUS ===")
    print(corpus)

    print("\n=== Tri par date ===")
    corpus.afficher_par_date(n=10)

    print("\n=== Tri par titre ===")
    corpus.afficher_par_titre(n=10)

    print("\n=== Sauvegarde ===")
    corpus.save("corpus_v1_export.tsv")
    print("Export OK -> corpus_v1_export.tsv")

if __name__ == "__main__":
    main()
