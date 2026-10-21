"""Embedding generation with a swappable provider (local or OpenAI)."""
from .config import settings


class Embedder:
    def __init__(self, provider: str | None = None):
        self.provider = provider or settings.embedding_provider
        if self.provider == "local":
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(settings.local_embedding_model)
        elif self.provider == "openai":
            from openai import OpenAI

            self._client = OpenAI()
        else:
            raise ValueError(f"Unknown EMBEDDING_PROVIDER: {self.provider}")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        if self.provider == "local":
            return self._model.encode(texts, normalize_embeddings=True).tolist()
        out: list[list[float]] = []
        for i in range(0, len(texts), 100):  # batch to respect API limits
            resp = self._client.embeddings.create(
                model=settings.openai_embedding_model, input=texts[i : i + 100]
            )
            out.extend(d.embedding for d in resp.data)
        return out

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]
