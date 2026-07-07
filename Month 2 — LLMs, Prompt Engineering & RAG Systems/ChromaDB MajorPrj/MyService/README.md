# 🚗 Automobile Workshop Customer Support Chatbot (RAG)

A local, high-performance **Retrieval-Augmented Generation (RAG)** chatbot for automobile workshop customer support. It grounds every answer in a curated knowledge base of vehicle problems and solutions, retrieved semantically and passed to a fast open-weight LLM served by Cerebras — no hallucinated repair advice.

---

## ✨ Features

- **Semantic retrieval** over a workshop knowledge base using local sentence embeddings — finds relevant documents even when the customer's wording differs from the stored text.
- **Persistent local vector store** (ChromaDB) — no external database service required.
- **Ultra-low-latency generation** via the Cerebras API running an open-weight LLM (`gpt-oss-120b`).
- **Strict grounding** — the assistant is instructed to answer only from retrieved context and to say so explicitly when it can't find an answer, instead of guessing.
- **Command-line chat interface** with a continuous conversation loop.
- **Conversation logging** — every query and response is stored in memory during the session and persisted to `chat_history.json` on exit.

---

## 🧱 Tech Stack

| Component            | Purpose                                      |
|-----------------------|-----------------------------------------------|
| Pandas                | Loading and cleaning the knowledge base CSV  |
| Sentence Transformers | Generating dense semantic embeddings (`all-MiniLM-L6-v2`) |
| ChromaDB              | Local, persistent vector storage and similarity search |
| Cerebras API (OpenAI-compatible) | Fast LLM inference for response generation |
| python-dotenv         | Loading API keys from a `.env` file          |

---

## 📂 Project Structure

```
.
├── service.ipynb                     # Main notebook: full RAG pipeline
├── customer_support_dataset.csv      # Knowledge base (vehicle, problem, solution, etc.)
├── automobile_workshop_vector_db/    # ChromaDB persistent storage (auto-created)
├── chat_history.json                 # Saved conversation logs (auto-created)
├── .env                               # Cerebras API key (not committed)
└── README.md
```

---

## 📊 Dataset Format

`customer_support_dataset.csv` should contain at least the following columns:

| Column         | Description                                  |
|----------------|-----------------------------------------------|
| `id`           | Unique identifier for each record             |
| `vehicle`      | Vehicle make/model the record applies to      |
| `category`     | Issue category (e.g. Engine, Brakes, Electrical) |
| `problem`      | Description of the customer-facing problem    |
| `solution`     | Recommended fix or advice                     |
| `keywords`     | Searchable keywords related to the issue      |
| `severity`     | Issue severity level                          |
| `source`       | Origin of the record (manual, technician notes, etc.) |
| `last_updated` | Date the record was last reviewed             |

---

## ⚙️ Setup

### 1. Clone / download the project

Place `service.ipynb` and `customer_support_dataset.csv` in the same directory.

### 2. Install dependencies

```bash
pip install pandas chromadb sentence-transformers python-dotenv openai
```

### 3. Configure your Cerebras API key

Create a `.env` file in the project root:

```
CEREBRAS_API_KEY=your_api_key_here
```

### 4. Run the notebook

Open `service.ipynb` in Jupyter and run all cells top to bottom:

```bash
jupyter notebook service.ipynb
```

The notebook will:
1. Load and clean the dataset
2. Build searchable documents and generate embeddings
3. Store embeddings in a local ChromaDB collection
4. Initialize the Cerebras LLM client
5. Launch an interactive command-line chatbot

---

## 💬 Usage

Once the chatbot launches, type your question at the prompt:

```
👤 You: My Tata Nexon engine is overheating.

🤖 Assistant: Checking our workshop database... 🔍
🤖 Assistant: [Grounded answer based on retrieved workshop records]
```

Type `exit`, `quit`, or `bye` to end the session. On exit, the full conversation for that session is saved to `chat_history.json`.

### Example queries

- "My Tata Nexon engine is overheating."
- "Why are my brakes making noise?"
- "How often should I change engine oil?"
- "My battery keeps draining overnight."
- "Why is my car vibrating while idling?"

If a question falls outside the knowledge base (e.g. asking about something unrelated to automobiles), the assistant will say it couldn't find relevant information rather than guessing.

---

## 🗃️ Conversation History

Every query and response pair is stored in an in-memory `conversation_history` list during the session and written to `chat_history.json` when the session ends (via `exit`/`quit`/`bye` or `Ctrl+C`). Each run appends a new session record rather than overwriting previous history, so the file accumulates a full log across runs:

```json
[
  {
    "session_timestamp": "2026-07-07T10:15:00",
    "turns": [
      { "query": "My battery keeps draining overnight.", "response": "..." }
    ]
  }
]
```

---

## 🔧 Known Fixes Applied

- Added the missing `retrieve_relevant_context()` function (Step 9), which is required by the pipeline but was previously undefined, causing every query to silently fail and return a generic error.
- Added session-level conversation history storage and JSON persistence so queries and responses are no longer discarded after being printed.

---

## 📖 How It Works (Pipeline)

```
User Query
   │
   ▼
Generate Query Embedding
   │
   ▼
Search ChromaDB (cosine similarity)
   │
   ▼
Retrieve Top-K Documents
   │
   ▼
Construct Grounded Prompt
   │
   ▼
Send to Cerebras LLM
   │
   ▼
Generate & Return Response
   │
   ▼
Store Query + Response in History
```

---

## 📌 Notes

- The embedding model (`all-MiniLM-L6-v2`) runs entirely locally — no API calls or costs for retrieval.
- Only the final generation step calls the Cerebras API.
- The system prompt strictly limits the LLM to the retrieved context, minimizing hallucinated repair advice.
