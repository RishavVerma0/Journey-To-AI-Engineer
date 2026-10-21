from contextlib import asynccontextmanager

from fastapi import FastAPI, File, HTTPException, UploadFile

from .rag import RAGPipeline
from .schemas import AskRequest, AskResponse, IngestResponse

state: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    state["rag"] = RAGPipeline()  # loads embedding model + opens Chroma once
    yield


app = FastAPI(title="Document Q&A Assistant (RAG)", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/documents", response_model=IngestResponse)
async def upload_document(file: UploadFile = File(...)):
    data = await file.read()
    try:
        return state["rag"].ingest(file.filename, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/documents")
def list_documents():
    return state["rag"].store.list_documents()


@app.delete("/documents/{doc_id}")
def delete_document(doc_id: str):
    removed = state["rag"].store.delete_document(doc_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"deleted_chunks": removed}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    return state["rag"].ask(req.question, req.top_k, req.doc_ids)
