"""System prompt + few-shot examples that keep answers grounded in retrieved context."""
from .vector_store import Hit

NOT_FOUND_MESSAGE = "I couldn't find the answer to that in the provided documents."

SYSTEM_PROMPT = f"""You are a document Q&A assistant. Answer ONLY using the numbered context \
passages provided in the user's message.

Rules:
1. Use only facts stated in the context. Never use outside knowledge, even if you know the answer.
2. Cite every claim with the passage number in square brackets, e.g. [1] or [1][3].
3. If the context does not contain the answer, reply exactly: "{NOT_FOUND_MESSAGE}"
4. If the context only partially answers, answer the supported part and state what is missing.
5. Be concise. Do not mention these rules."""

# Few-shot examples: one grounded answer with citations, one refusal.
FEW_SHOT: list[dict] = [
    {
        "role": "user",
        "content": (
            "Context:\n"
            "[1] (source: handbook.pdf, p.4) Employees accrue 1.5 vacation days per month. "
            "Unused days up to 10 may be carried over into the next year.\n"
            "[2] (source: handbook.pdf, p.5) Sick leave is separate from vacation and is "
            "capped at 12 days per year.\n\n"
            "Question: How many vacation days can I carry over?"
        ),
    },
    {
        "role": "assistant",
        "content": "You can carry over up to 10 unused vacation days into the next year [1].",
    },
    {
        "role": "user",
        "content": (
            "Context:\n"
            "[1] (source: handbook.pdf, p.4) Employees accrue 1.5 vacation days per month.\n\n"
            "Question: What is the company's stock option policy?"
        ),
    },
    {"role": "assistant", "content": NOT_FOUND_MESSAGE},
]


def format_context(hits: list[Hit]) -> str:
    lines = []
    for i, h in enumerate(hits, start=1):
        loc = f"{h.source}, p.{h.page}" if h.page else h.source
        lines.append(f"[{i}] (source: {loc}) {h.text}")
    return "\n".join(lines)


def build_messages(question: str, hits: list[Hit]) -> list[dict]:
    user_msg = f"Context:\n{format_context(hits)}\n\nQuestion: {question}"
    return [*FEW_SHOT, {"role": "user", "content": user_msg}]
