# IPL Match Information Retrieval System using ChromaDB

An AI-powered semantic search system for IPL match data that enables users to ask natural language questions about historical IPL matches. The project cleans IPL datasets, converts match records into searchable documents, stores them in ChromaDB with vector embeddings, and retrieves the most relevant matches using semantic similarity.

---

## Features

- Cleans and standardizes IPL match datasets
- Handles franchise name changes and inconsistent data
- Converts match records into natural language documents
- Stores match embeddings in ChromaDB
- Uses Sentence Transformers for semantic search
- Retrieves the most relevant IPL matches for any user query
- Generates answers using an LLM (Cerebras/OpenAI-compatible API)

---

## Project Workflow

```
Raw IPL Dataset
        │
        ▼
Data Cleaning
        │
        ▼
Document Serialization
        │
        ▼
Sentence Embeddings
        │
        ▼
ChromaDB Vector Database
        │
        ▼
Semantic Search
        │
        ▼
LLM Answer Generation
```

---

## Technologies Used

- Python
- Pandas
- NumPy
- ChromaDB
- Sentence Transformers
- OpenAI SDK
- Cerebras API
- python-dotenv

---

## Project Structure

```
.
├── ipl_DB.ipynb          # Main notebook
├── ipl.csv               # IPL dataset
├── ipl_chromadb/         # Persistent Chroma database
├── .env                  # API key configuration
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

Install dependencies:

```bash
pip install pandas numpy chromadb sentence-transformers python-dotenv openai
```

---

## Environment Variables

Create a `.env` file:

```env
API_KEY=your_cerebras_api_key
```

The notebook uses the Cerebras API through the OpenAI-compatible SDK.

---

## Dataset Preparation

Place the IPL dataset in the project directory.

Example:

```
ipl.csv
```

The notebook loads the dataset using:

```python
df_real_raw = pd.read_csv("ipl.csv")
```

---

## Data Cleaning

The notebook includes a cleaning pipeline that:

- Standardizes team names
- Handles missing values
- Fixes franchise name inconsistencies
- Parses squad information
- Cleans Super Over records
- Produces consistent metadata for vector search

Main function:

```python
clean_ipl_dataset(df)
```

---

## Document Serialization

Each cleaned match is transformed into:

- A natural language document
- Structured metadata

Example:

```
IPL 2024:
Chennai Super Kings defeated Mumbai Indians by 20 runs at Chennai.
```

Main function:

```python
serialize_row_for_chromadb()
```

---

## Building the Vector Database

The project uses:

- **ChromaDB** for vector storage
- **all-MiniLM-L6-v2** for text embeddings

Documents are embedded and stored with metadata for efficient retrieval.

---

## Semantic Search

Example:

```python
results = semantic_search(
    "Which matches did CSK win in Chennai?"
)
```

The system returns the most semantically relevant IPL matches rather than relying on exact keyword matching.

---

## Question Answering

Retrieved match documents are passed to an LLM along with the user's question.

Example:

```python
answer_question(
    "How many matches did CSK win against MI?"
)
```

The LLM is instructed to answer **only using the retrieved context**, reducing hallucinations.

---

## Example Questions

- Which matches did CSK win in Chennai?
- How many matches did MI lose in 2022?
- Who won the IPL final in 2023?
- Which team defeated RCB the most?
- Show matches played at Wankhede Stadium.
- Which matches went to a Super Over?
- How many matches were won by more than 100 runs?
- Which matches did KKR win while chasing?

---

## Key Functions

| Function | Description |
|----------|-------------|
| `clean_ipl_dataset()` | Cleans raw IPL data |
| `serialize_row_for_chromadb()` | Converts matches into searchable documents |
| `semantic_search()` | Performs vector similarity search |
| `build_context()` | Builds LLM context from retrieved matches |
| `answer_question()` | Generates the final answer |

---

## Future Improvements

- Streamlit web application
- FastAPI backend
- Hybrid search (keyword + semantic)
- Player statistics retrieval
- Match visualization dashboard
- RAG evaluation metrics
- Support for multiple embedding models
- Docker deployment

---

## Sample Pipeline

```text
User Question
      │
      ▼
Generate Embedding
      │
      ▼
Search ChromaDB
      │
      ▼
Retrieve Top Matches
      │
      ▼
Build Context
      │
      ▼
LLM
      │
      ▼
Final Answer
```

---

## License

This project is intended for educational and research purposes.

---

## Author

Developed as an **IPL Match Information Retrieval System** demonstrating Retrieval-Augmented Generation (RAG), semantic search, vector databases, and LLM-powered question answering.