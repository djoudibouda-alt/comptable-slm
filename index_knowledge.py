import os
from rag_pipeline import RAGPipeline


def index_all():
    pipeline = RAGPipeline()
    knowledge_dir = os.path.join(os.path.dirname(__file__), "knowledge_base")

    if not os.path.isdir(knowledge_dir):
        print(f"Erreur: dossier '{knowledge_dir}' non trouvé.")
        return

    files = sorted([f for f in os.listdir(knowledge_dir) if f.endswith(".txt")])

    if not files:
        print("Aucun fichier .txt trouvé dans knowledge_base/.")
        return

    print(f"Indexation de {len(files)} fichiers...\n")

    total_chunks = 0
    for filename in files:
        filepath = os.path.join(knowledge_dir, filename)
        try:
            n_chunks = pipeline.index_file(filepath)
            total_chunks += n_chunks
            print(f"  [OK] {filename} -> {n_chunks} chunks")
        except Exception as e:
            print(f"  [ERREUR] {filename} -> {e}")

    total_in_db = pipeline.vector_store.count()
    print(f"\nTerminé: {total_chunks} chunks indexés.")
    print(f"Total dans la base: {total_in_db} chunks.")


if __name__ == "__main__":
    index_all()
