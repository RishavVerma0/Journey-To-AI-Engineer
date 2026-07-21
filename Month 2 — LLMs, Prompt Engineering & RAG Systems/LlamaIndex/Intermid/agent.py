"""Builds the RAG query engine (with the relevance guardrail) and wraps it
as a tool-calling agent. Import `build_agent()` from here — see main.py."""

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
    "You are a Maruti Suzuki assistant. Answer ONLY using the context below.\n"
    f'If the context does not contain the answer, respond exactly with: "{FALLBACK_MESSAGE}"\n\n'
    "Context:\n{context_str}\n\nQuestion: {query_str}\nAnswer:"
)

SYSTEM_PROMPT = (
    "You are a Maruti Suzuki assistant. You must ONLY answer questions about "
    "Maruti showrooms, service centers, workshops, FAQs, and policies, and ONLY "
    "using information returned by the maruti_knowledge_base tool. If the tool "
    "returns no relevant information, or the question is unrelated to Maruti "
    "(general knowledge, other car brands, unrelated topics), reply exactly: "
    f'"{FALLBACK_MESSAGE}" Never guess or use outside knowledge.'
)


def load_index() -> VectorStoreIndex:
    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    chroma_collection = chroma_client.get_or_create_collection(CHROMA_COLLECTION)
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
            "Use this for ANY question about Maruti Suzuki showrooms, service "
            "centers, workshops, FAQs, or policies. Always call this tool before "
            "answering — never answer from general knowledge."
        ),
    )

    return FunctionAgent(
        tools=[maruti_tool],  # add more tools here later, e.g. dealership_locator_tool
        llm=Settings.llm,
        system_prompt=SYSTEM_PROMPT,
    )