from Corpus import Corpus
from DocumentFactory import DocumentFactory
from SearchEngine import SearchEngine

def main():
    corpus = Corpus.get_instance("Corpus TD7")
    if not corpus.id2doc:
        factory = DocumentFactory()
        corpus.load("corpus_td6.tsv", factory)

    engine = SearchEngine(
        corpus,
        preprocessor=Corpus.nettoyer_texte,
        stop_words="english"
    ).build()

    print("=== Résultats TD7 (TF-IDF) ===")
    print(engine.search("climate", n=10))

if __name__ == "__main__":
    main()
