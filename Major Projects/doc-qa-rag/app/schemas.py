from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3)
    top_k: int | None = Field(None, ge=1, le=20)
    doc_ids: list[str] | None = None


class Source(BaseModel):
    id: int
    source: str
    doc_id: str
    page: int | None
    similarity: float
    cited: bool
    snippet: str


class AskResponse(BaseModel):
    answer: str
    grounded: bool
    sources: list[Source]


class IngestResponse(BaseModel):
    doc_id: str
    source: str
    chunks: int
