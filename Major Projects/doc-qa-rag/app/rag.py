"""The RAG pipeline: ingest -> retrieve -> generate with citations."""
import hashlib
import re

from .chunking import chunk_pages
from .config import settings
from .embeddings import Embedder
from .llm import LLM
from .loaders import load_document
from .prompts import NOT_FOUND_MESSAGE, SYSTEM_PROMPT, build_messages
from .vector_store import Hit, VectorStore


def extract_cited_numbers(answer: str) -> set[int]:
    return {int(n) for n in re.findall(r"\[(\d+)\]", answer)}


class RAGPipeline:
    def __init__(self, embedder=None, store=None, llm=None):
        self.embedder = embedder or Embedder()
        self.store = store or VectorStore()
        self.llm = llm or LLM()

    # ---------- ingestion ----------
    def ingest(self, filename: str, data: bytes) -> dict:
        pages = load_document(filename, data)
        chunks = chunk_pages(pages, settings.chunk_size, settings.chunk_overlap)
        if not chunks:
            raise ValueError("No extractable text found in the document.")
        doc_id = hashlib.sha256(data).hexdigest()[:16]
        embeddings = self.embedder.embed_documents([c.text for c in chunks])
        self.store.add_document(doc_id, filename, chunks, embeddings)
        return {"doc_id": doc_id, "source": filename, "chunks": len(chunks)}

    # ---------- question answering ----------
    def ask(self, question: str, top_k: int | None = None, doc_ids: list[str] | None = None) -> dict:
        top_k = top_k or settings.top_k
        hits = self.store.query(self.embedder.embed_query(question), top_k, doc_ids)
        hits = [h for h in hits if h.similarity >= settings.min_similarity]

        # Guardrail #1: nothing relevant retrieved -> don't even call the LLM.
        if not hits:
            return {"answer": NOT_FOUND_MESSAGE, "grounded": False, "sources": []}

        answer = self.llm.generate(SYSTEM_PROMPT, build_messages(question, hits))
        cited = extract_cited_numbers(answer)
        return {
            "answer": answer,
            "grounded": answer.strip() != NOT_FOUND_MESSAGE,
            "sources": [self._source(i, h, i in cited) for i, h in enumerate(hits, start=1)],
        }

    @staticmethod
    def _source(n: int, h: Hit, cited: bool) -> dict:
        return {
            "id": n,
            "source": h.source,
            "doc_id": h.doc_id,
            "page": h.page,
            "similarity": round(h.similarity, 3),
            "cited": cited,
            "snippet": h.text[:300],
        }
