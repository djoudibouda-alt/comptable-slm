import os
import uuid
import re
from openai import OpenAI
from embedding import EmbeddingService
from vector_store import VectorStore
from config import (
    NVIDIA_API_KEY,
    NVIDIA_BASE_URL,
    LLM_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K,
    USE_LOCAL_LLM,
    LOCAL_LLM_URL,
)


class RAGPipeline:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

        if USE_LOCAL_LLM:
            self.llm_client = OpenAI(
                base_url=LOCAL_LLM_URL,
                api_key="ollama",
            )
        else:
            self.llm_client = OpenAI(
                api_key=NVIDIA_API_KEY,
                base_url=NVIDIA_BASE_URL,
            )

    def chunk_by_sections(self, text: str, source: str = "unknown") -> list[dict]:
        sections = []
        current_section = ""
        current_title = "Introduction"

        for line in text.split("\n"):
            if line.startswith("## ") or line.startswith("### "):
                if current_section.strip():
                    sections.append({
                        "title": current_title,
                        "content": current_section.strip(),
                        "source": source,
                    })
                current_title = line.strip("# ").strip()
                current_section = line + "\n"
            else:
                current_section += line + "\n"

        if current_section.strip():
            sections.append({
                "title": current_title,
                "content": current_section.strip(),
                "source": source,
            })

        return sections

    def index_document(self, document: str, source: str = "unknown"):
        sections = self.chunk_by_sections(document, source)
        if not sections:
            return 0

        texts = [s["content"] for s in sections]
        embeddings = self.embedding_service.embed_documents(texts)
        ids = [str(uuid.uuid4()) for _ in sections]
        metadatas = [{"source": s["source"], "title": s["title"]} for s in sections]
        self.vector_store.add_documents(ids, texts, embeddings, metadatas)
        return len(sections)

    def index_file(self, file_path: str) -> int:
        filename = os.path.basename(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return self.index_document(content, source=filename)

    def retrieve(self, query: str) -> list[dict]:
        query_embedding = self.embedding_service.embed_query(query)
        results = self.vector_store.search(query_embedding, top_k=TOP_K)
        filtered = [
            {"document": doc, "distance": dist, "source": meta.get("source", ""), "title": meta.get("title", "")}
            for doc, dist, meta in zip(
                results["documents"],
                results["distances"],
                results.get("metadatas", [{}] * len(results["documents"]))
            )
            if dist < 0.6
        ]
        return filtered

    def generate(self, query: str, context_docs: list[dict]) -> str:
        context_parts = []
        for doc in context_docs:
            source = doc.get("source", "")
            title = doc.get("title", "")
            context_parts.append(f"[Source: {source} | Section: {title}]\n{doc['document']}")
        context = "\n\n---\n\n".join(context_parts)

        prompt = (
            "Tu es un expert-comptable et auditeur algérien. "
            "Tu utilises le Système Comptable et Financier (SCF) algérien.\n"
            "Réponds TOUJOURS en français, de manière précise et professionnelle.\n\n"
            "IMPORTANT :\n"
            "- Utilise UNIQUEMENT les informations du contexte ci-dessous pour répondre.\n"
            "- Ne jamais inventer d'informations.\n"
            "- Si le contexte ne contient pas la réponse, dis-le clairement.\n"
            "- Formule ta réponse de manière claire et structurée.\n\n"
            f"=== CONTEXTE DE LA BASE DE CONNAISSANCES ===\n{context}\n=== FIN DU CONTEXTE ===\n\n"
            f"QUESTION : {query}\n\n"
            "RÉPONSE (en français, précise et détaillée) :"
        )

        response = self.llm_client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1024,
        )
        return response.choices[0].message.content

    def query(self, question: str) -> dict:
        results = self.retrieve(question)
        answer = self.generate(question, results)
        return {
            "answer": answer,
            "sources": results,
        }
