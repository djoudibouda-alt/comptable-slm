import os
import sys
from rag_pipeline import RAGPipeline
from index_knowledge import index_all


def print_sources(sources: list[dict]):
    for i, source in enumerate(sources, 1):
        score = 1 - source["distance"]
        doc = source["document"][:200]
        print(f"  [{i}] Score: {score:.4f}")
        print(f"      {doc}...")
        print()


def main():
    pipeline = RAGPipeline()

    print("=== Nemotron RAG Pipeline ===")
    print("Commandes: 'index <fichier>', 'index-all', 'ask <question>', 'quit'\n")

    while True:
        try:
            user_input = input(">> ").strip()
            if user_input.startswith(">> "):
                user_input = user_input[2:].strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAu revoir !")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("Au revoir !")
            break

        if user_input.lower().startswith("index "):
            file_path = user_input[6:].strip()
            if not os.path.isfile(file_path):
                print(f"Erreur: fichier '{file_path}' non trouvé.\n")
                continue
            try:
                n_chunks = pipeline.index_file(file_path)
                total = pipeline.vector_store.count()
                print(f"Indexé {n_chunks} chunks depuis '{file_path}'.")
                print(f"Total dans la base: {total} chunks.\n")
            except Exception as e:
                print(f"Erreur lors de l'indexation: {e}\n")

        elif user_input.lower() == "index-all":
            try:
                index_all()
            except Exception as e:
                print(f"Erreur: {e}\n")

        elif user_input.lower().startswith("ask "):
            question = user_input[4:].strip()
            if not question:
                print("Veuillez poser une question.\n")
                continue
            try:
                print("Recherche en cours...")
                result = pipeline.query(question)
                print(f"\nRéponse:\n{result['answer']}\n")
                print("Sources:")
                print_sources(result["sources"])
            except Exception as e:
                print(f"Erreur: {e}\n")

        else:
            print("Commande inconnue. Utilisez 'index <fichier>', 'index-all', 'ask <question>', ou 'quit'.\n")


if __name__ == "__main__":
    main()
