import os
from openai import OpenAI


def get_client(provider: str):
    """
    Returns (OpenAI-compatible client, model name) for the given provider.
    Anthropic is NOT handled here — use get_anthropic_client() instead.
    """
    provider = provider.lower().strip()

    if provider == "openai":
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        return client, "gpt-4o-mini"

    elif provider == "groq":
        client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1",
        )
        return client, "llama-3.1-8b-instant"

    # elif provider == "cerebras":
    #     client = OpenAI(
    #         api_key=os.getenv("CEREBRAS_API_KEY"),
    #         base_url="https://api.cerebras.ai/v1",
    #     )
    #     return client, "llama3.1-8b"

    else:
        raise ValueError(
            f"Unknown provider: '{provider}'. "
            "Choose from: openai, groq, cerebras, anthropic"
        )


def get_anthropic_client():
    """Returns an Anthropic client. Kept separate because it uses a different SDK."""
    import anthropic
    return anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))