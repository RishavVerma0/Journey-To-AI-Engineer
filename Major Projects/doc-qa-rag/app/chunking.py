"""Split pages into overlapping chunks, keeping source metadata."""
from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter

from .loaders import Page


@dataclass
class Chunk:
    text: str
    chunk_index: int
    page: int | None


def chunk_pages(pages: list[Page], chunk_size: int, chunk_overlap: int) -> list[Chunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks: list[Chunk] = []
    for page in pages:
        for piece in splitter.split_text(page.text):
            piece = piece.strip()
            if piece:
                chunks.append(Chunk(text=piece, chunk_index=len(chunks), page=page.page))
    return chunks
