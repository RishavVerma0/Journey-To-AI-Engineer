"""Central configuration for the Maruti RAG agent project."""
from pathlib import Path
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.node_parser import SentenceSplitter

# --- Models (must be pulled via `ollama pull <model>` first) ---
LLM_MODEL = "ollama:qwen2.5:3b"
EMBED_MODEL = "nomic-embed-text"

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = "./chroma_db"
CHROMA_COLLECTION = "maruti_docs"

# --- Chunking ---
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

# --- Retrieval / guardrail tuning ---
SIMILARITY_TOP_K = 3
SIMILARITY_CUTOFF = 0.55  # tune against your own test queries, see README

FALLBACK_MESSAGE = "Sorry, I can't answer your question."


def configure_global_settings():
    """Wire up the LLM, embedding model, and chunker used everywhere in the project."""
    Settings.llm = Ollama(model=LLM_MODEL, request_timeout=120.0)
    Settings.embed_model = OllamaEmbedding(model_name=EMBED_MODEL)
    Settings.node_parser = SentenceSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )