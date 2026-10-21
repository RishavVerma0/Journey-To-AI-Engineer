"""Thin wrapper around a persistent ChromaDB collection (cosine similarity)."""
from dataclasses import dataclass

import chromadb

from .chunking import Chunk
from .config import settings


@dataclass
class Hit:
    text: str
    source: str
    doc_id: str
    page: int | None
    chunk_index: int
    similarity: float  # 1.0 = identical, higher is better


class VectorStore:
    def __init__(self, path: str | None = None):
        self._client = chromadb.PersistentClient(path=path or settings.chroma_path)
        self._col = self._client.get_or_create_collection(
            name="documents", metadata={"hnsw:space": "cosine"}
        )

    def add_document(
        self, doc_id: str, source: str, chunks: list[Chunk], embeddings: list[list[float]]
    ) -> None:
        self.delete_document(doc_id)  # re-ingesting the same file replaces it
        self._col.add(
            ids=[f"{doc_id}:{c.chunk_index}" for c in chunks],
            documents=[c.text for c in chunks],
            embeddings=embeddings,
            metadatas=[
                {
                    "doc_id": doc_id,
                    "source": source,
                    "chunk_index": c.chunk_index,
                    "page": c.page if c.page is not None else -1,
                }
                for c in chunks
            ],
        )

    def query(self, embedding: list[float], k: int, doc_ids: list[str] | None = None) -> list[Hit]:
        where = {"doc_id": {"$in": doc_ids}} if doc_ids else None
        res = self._col.query(query_embeddings=[embedding], n_results=k, where=where)
        hits = []
        for text, meta, dist in zip(
            res["documents"][0], res["metadatas"][0], res["distances"][0]
        ):
            hits.append(
                Hit(
                    text=text,
                    source=meta["source"],
                    doc_id=meta["doc_id"],
                    page=meta["page"] if meta["page"] != -1 else None,
                    chunk_index=meta["chunk_index"],
                    similarity=1.0 - dist,
                )
            )
        return hits

    def list_documents(self) -> list[dict]:
        metas = self._col.get(include=["metadatas"])["metadatas"]
        docs: dict[str, dict] = {}
        for m in metas:
            d = docs.setdefault(m["doc_id"], {"doc_id": m["doc_id"], "source": m["source"], "chunks": 0})
            d["chunks"] += 1
        return list(docs.values())

    def delete_document(self, doc_id: str) -> int:
        existing = self._col.get(where={"doc_id": doc_id})["ids"]
        if existing:
            self._col.delete(ids=existing)
        return len(existing)
