"""Central configuration for the Maruti RAG agent project."""
from pathlib import Path
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.node_parser import SentenceSplitter

# --- Models (must be pulled via `ollama pull <model>` first) ---
LLM_MODEL = "qwen2.5:3b"
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

# IMPORTANT: this cutoff assumes COSINE similarity (higher = better, range ~0-1).
# We force Chroma to use cosine distance (see ingest.py / agent.py:
# metadata={"hnsw:space": "cosine"}) so this threshold is meaningful.
# If that metadata setting is ever removed, Chroma defaults to L2 distance
# (lower = better, often > 1) and this cutoff will silently filter out every result.
SIMILARITY_CUTOFF = 0.3

FALLBACK_MESSAGE = "Sorry, I can't answer your question."

# Ollama can be slow on first load / CPU-only boxes. Keep this generous.
LLM_REQUEST_TIMEOUT = 300.0


def configure_global_settings():
    """Wire up the LLM, embedding model, and chunker used everywhere in the project."""
    Settings.llm = Ollama(model=LLM_MODEL, request_timeout=LLM_REQUEST_TIMEOUT)
    Settings.embed_model = OllamaEmbedding(model_name=EMBED_MODEL)
    Settings.node_parser = SentenceSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )