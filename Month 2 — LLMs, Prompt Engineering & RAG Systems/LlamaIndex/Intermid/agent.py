"""Builds the RAG query engine (with a relaxed relevance guardrail) and wraps it
as a tool-calling agent. Import `build_agent()` from here — see main.py.
"""

import chromadb
from llama_index.core import Settings, VectorStoreIndex, PromptTemplate
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.tools import QueryEngineTool
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.vector_stores.chroma import ChromaVectorStore

from config import (
    configure_global_settings,
    CHROMA_DIR,
    CHROMA_COLLECTION,
    SIMILARITY_TOP_K,
    SIMILARITY_CUTOFF,
    FALLBACK_MESSAGE,
)

QA_PROMPT = PromptTemplate(
    "Context information is provided below:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Using ONLY the context above, answer the question: {query_str}\n"
    f'If the information is not present in the context, reply exactly: "{FALLBACK_MESSAGE}"'
)

SYSTEM_PROMPT = (
    "You are an official Maruti Suzuki assistant. "
    "Your duty is to answer questions about Maruti Suzuki showrooms, service centers, "
    "workshops, FAQs, and policies. "
    "ALWAYS call the `maruti_knowledge_base` tool to retrieve relevant context before answering. "
    "Never answer using outside knowledge or assumptions. "
    f'If the tool returns no useful context, respond with: "{FALLBACK_MESSAGE}"'
)


def load_index() -> VectorStoreIndex:
    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Must match the metric set at creation time in ingest.py, or Chroma will
    # raise/ignore the metadata (collection settings are fixed at creation).
    chroma_collection = chroma_client.get_or_create_collection(
        CHROMA_COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )

    count = chroma_collection.count()
    if count == 0:
        print(
            f"[Warning] Chroma collection '{CHROMA_COLLECTION}' is empty! "
            f"Run `python ingest.py` first."
        )
    else:
        print(f"[Info] Loaded Chroma collection '{CHROMA_COLLECTION}' with {count} chunks.")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    return VectorStoreIndex.from_vector_store(vector_store)


def build_agent() -> FunctionAgent:
    configure_global_settings()
    index = load_index()

    query_engine = index.as_query_engine(
        similarity_top_k=SIMILARITY_TOP_K,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=SIMILARITY_CUTOFF)],
        text_qa_template=QA_PROMPT,
    )

    maruti_tool = QueryEngineTool.from_defaults(
        query_engine=query_engine,
        name="maruti_knowledge_base",
        description=(
            "Use this tool for ANY query related to Maruti Suzuki showrooms, service centers, "
            "workshops, booking rules, FAQs, or policies. Pass the user query directly as input."
        ),
    )

    return FunctionAgent(
        tools=[maruti_tool],
        llm=Settings.llm,
        system_prompt=SYSTEM_PROMPT,
    )