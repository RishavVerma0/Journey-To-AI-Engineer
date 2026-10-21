"""LLM call with a swappable provider."""
from .config import settings


class LLM:
    def __init__(self, provider: str | None = None):
        self.provider = provider or settings.llm_provider
        if self.provider == "anthropic":
            import anthropic

            self._client = anthropic.Anthropic()
        elif self.provider == "openai":
            from openai import OpenAI

            self._client = OpenAI()
        else:
            raise ValueError(f"Unknown LLM_PROVIDER: {self.provider}")

    def generate(self, system: str, messages: list[dict], max_tokens: int = 800) -> str:
        if self.provider == "anthropic":
            resp = self._client.messages.create(
                model=settings.anthropic_model,
                system=system,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0,
            )
            return "".join(b.text for b in resp.content if b.type == "text").strip()

        resp = self._client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "system", "content": system}, *messages],
            max_tokens=max_tokens,
            temperature=0,
        )
        return (resp.choices[0].message.content or "").strip()
