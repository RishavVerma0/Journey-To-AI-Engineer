"""Turn uploaded files into plain text 'pages' with metadata."""
import io
from dataclasses import dataclass


@dataclass
class Page:
    text: str
    page: int | None = None  # 1-based page number for PDFs, None otherwise


SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}


def load_document(filename: str, data: bytes) -> list[Page]:
    name = filename.lower()
    if name.endswith(".pdf"):
        return _load_pdf(data)
    if name.endswith((".txt", ".md")):
        return [Page(text=data.decode("utf-8", errors="ignore"))]
    raise ValueError(f"Unsupported file type. Supported: {sorted(SUPPORTED_EXTENSIONS)}")


def _load_pdf(data: bytes) -> list[Page]:
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(data))
    pages = []
    for i, p in enumerate(reader.pages, start=1):
        text = (p.extract_text() or "").strip()
        if text:
            pages.append(Page(text=text, page=i))
    return pages
