"""Run this once, and again whenever your documents change, to (re)build the
ChromaDB index that the agent queries at runtime.

    python ingest.py
"""

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

    documents = SimpleDirectoryReader(
        DATA_DIR,
        recursive=True,
        required_exts=[".pdf", ".docx", ".txt", ".csv"],
    ).load_data()

    if not documents:
        print(f"No documents found in '{DATA_DIR}'. Add files there and re-run.")
        return

    documents = [tag_category(d) for d in documents]
    print(f"Loaded {len(documents)} documents from '{DATA_DIR}'")

    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    chroma_collection = chroma_client.get_or_create_collection(CHROMA_COLLECTION)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    print(f"Indexed into ChromaDB collection '{CHROMA_COLLECTION}' at '{CHROMA_DIR}'")


if __name__ == "__main__":
    build_index()
