"""Offline tests: no API keys or model downloads required."""
from app.chunking import chunk_pages
from app.loaders import Page, load_document
from app.prompts import NOT_FOUND_MESSAGE, build_messages
from app.rag import RAGPipeline, extract_cited_numbers
from app.vector_store import Hit, VectorStore


class FakeEmbedder:
    """Deterministic bag-of-keywords embedder."""
    VOCAB = ["vacation", "sick", "salary", "remote"]

    def _vec(self, t):
        v = [float(t.lower().count(w)) for w in self.VOCAB]
        return v + [0.0] if any(v) else [0.0] * len(self.VOCAB) + [1.0]

    def embed_documents(self, texts): return [self._vec(t) for t in texts]
    def embed_query(self, t): return self._vec(t)


class FakeLLM:
    def generate(self, system, messages, max_tokens=800):
        return "You get 18 vacation days [1]."


def test_chunking_overlap_and_metadata():
    pages = [Page(text="word " * 500, page=2)]
    chunks = chunk_pages(pages, chunk_size=200, chunk_overlap=40)
    assert len(chunks) > 1
    assert all(c.page == 2 for c in chunks)
    assert [c.chunk_index for c in chunks] == list(range(len(chunks)))


def test_loader_text_and_unsupported():
    assert load_document("a.txt", b"hello")[0].text == "hello"
    try:
        load_document("a.exe", b"x")
        assert False
    except ValueError:
        pass


def test_prompt_contains_context_and_fewshot():
    hit = Hit("Vacation is 18 days.", "hr.md", "d1", None, 0, 0.9)
    msgs = build_messages("How many vacation days?", [hit])
    assert msgs[-1]["role"] == "user" and "[1] (source: hr.md)" in msgs[-1]["content"]
    assert msgs[3]["content"] == NOT_FOUND_MESSAGE  # refusal example present


def test_citation_parsing():
    assert extract_cited_numbers("A [1] and B [3][2].") == {1, 2, 3}


def test_pipeline_end_to_end(tmp_path):
    rag = RAGPipeline(FakeEmbedder(), VectorStore(str(tmp_path)), FakeLLM())
    info = rag.ingest("hr.md", b"Employees get 18 vacation days per year.")
    assert info["chunks"] == 1

    res = rag.ask("How many vacation days?")
    assert res["grounded"] and res["sources"][0]["cited"]

    # Off-topic question: nothing similar enough -> refusal without calling the LLM
    res = rag.ask("completely unrelated zebra question")
    assert res["answer"] == NOT_FOUND_MESSAGE and res["sources"] == []
