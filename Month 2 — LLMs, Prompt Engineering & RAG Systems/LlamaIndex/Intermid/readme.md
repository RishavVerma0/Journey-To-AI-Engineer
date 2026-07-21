# Maruti RAG Agent

A local RAG agent over Maruti workshop/showroom/service-center/FAQ/policy documents,
built with LlamaIndex + ChromaDB + Ollama. Off-topic questions get a fixed fallback
reply instead of a hallucinated answer.

## How it works

**Ingestion (run once, or whenever docs change)**
`data/` documents → chunked → embedded (Ollama) → stored in ChromaDB

**Query (every user question)**
question → agent → retriever (top-k + similarity cutoff) → either:
- relevant chunks found → Ollama LLM answers from that context
- nothing relevant found → fixed fallback: "Sorry, I can't answer your question."

Two independent safety nets keep it on-topic:
1. **Similarity cutoff** — if nothing in ChromaDB is close enough to the question,
   skip the LLM entirely and return the fallback.
2. **System prompt** — even when something is retrieved, the agent is told to only
   use that context and never its own general knowledge.

## Project layout

```
maruti-rag-agent/
├── data/              # put your Maruti documents here (pdf, docx, txt, csv)
├── config.py          # models, paths, chunking/retrieval settings
├── ingest.py          # builds the ChromaDB index — run this first
├── agent.py           # builds the query engine + agent with the guardrail
├── main.py            # CLI chat loop
└── requirements.txt
```

## Setup

1. Install Ollama (https://ollama.com), then pull the two models used here:
   ```bash
   ollama pull llama3.1
   ollama pull nomic-embed-text
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Copy your Maruti documents into `data/` (subfolders are fine).

4. Build the index (run again whenever you add/change documents):
   ```bash
   python ingest.py
   ```

5. Chat with the agent:
   ```bash
   python main.py
   ```

## Tuning the guardrail

`SIMILARITY_CUTOFF` in `config.py` (default `0.55`) controls how strict the
relevance filter is. Test it with a mix of questions and adjust:

- Too many off-topic questions get answered → raise the cutoff
- In-domain questions wrongly get the fallback → lower the cutoff

Good test set:
```
"What documents do I need for a free service?"   # in-domain
"What is the capital of India?"                   # out-of-domain
"Tell me about Hyundai service centers"           # out-of-domain, tricky
"What's your refund policy?"                      # in-domain
```

## Extending it

`agent.py` is structured so you can add more tools to the `tools=[...]` list
later — e.g. a dealership locator, a structured lookup by city, or an
escalation/ticket-creation tool — without changing the rest of the pipeline.