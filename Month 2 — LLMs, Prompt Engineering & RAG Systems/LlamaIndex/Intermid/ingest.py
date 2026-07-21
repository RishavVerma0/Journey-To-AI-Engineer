"""Run this once, and again whenever your documents change, to (re)build the
ChromaDB index that the agent queries at runtime.

    python ingest.py
"""

import shutil
from pathlib import Path

import chromadb
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore

from config import configure_global_settings, DATA_DIR, CHROMA_DIR, CHROMA_COLLECTION


def tag_category(doc):
    """Best-effort category tagging from filename. Not required for retrieval to
    work, but makes debugging and future filtering much easier."""
    name = doc.metadata.get("file_name", "").lower()
    if "faq" in name:
        doc.metadata["category"] = "faq"
    elif "polic" in name:
        doc.metadata["category"] = "policy"
    elif "service" in name or "workshop" in name:
        doc.metadata["category"] = "service_center"
    elif "showroom" in name:
        doc.metadata["category"] = "showroom"
    else:
        doc.metadata["category"] = "general"
    return doc


def build_index():
    configure_global_settings()

    data_path = Path(DATA_DIR)
    if not data_path.exists():
        print(f"Data directory '{DATA_DIR}' does not exist. Create it and add your files.")
        return

    documents = SimpleDirectoryReader(
        str(DATA_DIR),
        recursive=True,
        required_exts=[".pdf", ".docx", ".txt", ".csv"],
    ).load_data()

    if not documents:
        print(f"No documents found in '{DATA_DIR}'. Add files there and re-run.")
        return

    documents = [tag_category(d) for d in documents]
    print(f"Loaded {len(documents)} documents from '{DATA_DIR}'")

    # Wipe any old index so we never mix an old distance-metric collection
    # with a new one — this is the #1 cause of "the agent gets no hits" bugs.
    chroma_path = Path(CHROMA_DIR)
    if chroma_path.exists():
        print(f"Removing existing Chroma store at '{CHROMA_DIR}' for a clean rebuild...")
        shutil.rmtree(chroma_path)

    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Force cosine similarity so SIMILARITY_CUTOFF in config.py behaves as expected.
    # Chroma's default is L2 distance (lower = better, unbounded), which silently
    # breaks any cutoff logic written for cosine similarity (higher = better, 0-1).
    chroma_collection = chroma_client.get_or_create_collection(
        CHROMA_COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    VectorStoreIndex.from_documents(documents, storage_context=storage_context)

    print(f"Indexed into ChromaDB collection '{CHROMA_COLLECTION}' at '{CHROMA_DIR}'")
    print(f"Collection now has {chroma_collection.count()} chunks.")


if __name__ == "__main__":
    build_index()