from openai import OpenAI
from config import NVIDIA_API_KEY, NVIDIA_BASE_URL, EMBEDDING_MODEL


class EmbeddingService:
    def __init__(self):
        self.client = OpenAI(
            api_key=NVIDIA_API_KEY,
            base_url=NVIDIA_BASE_URL,
        )
        self.model = EMBEDDING_MODEL

    def embed_texts(self, texts: list[str], input_type: str = "passage") -> list[list[float]]:
        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
            encoding_format="float",
            extra_body={"input_type": input_type},
        )
        return [item.embedding for item in response.data]

    def embed_query(self, query: str) -> list[float]:
        return self.embed_texts([query], input_type="query")[0]

    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        return self.embed_texts(documents, input_type="passage")
