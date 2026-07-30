import chromadb
from config import EMBEDDING_DIMENSIONS, TOP_K
import os


class VectorStore:
    def __init__(self, collection_name: str = "nemotron_rag"):
        persist_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_documents(self, ids: list[str], documents: list[str], embeddings: list[list[float]], metadatas: list[dict] = None):
        kwargs = {
            "ids": ids,
            "documents": documents,
            "embeddings": embeddings,
        }
        if metadatas:
            kwargs["metadatas"] = metadatas
        self.collection.add(**kwargs)

    def search(self, query_embedding: list[float], top_k: int = TOP_K) -> dict:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "distances", "metadatas"],
        )
        return {
            "documents": results["documents"][0],
            "distances": results["distances"][0],
            "metadatas": results["metadatas"][0] if results.get("metadatas") else [{}] * len(results["documents"][0]),
        }

    def count(self) -> int:
        return self.collection.count()

    def reset(self):
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
            metadata={"hnsw:space": "cosine"},
        )
