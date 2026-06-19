import os
from dotenv import load_dotenv
from providers import get_client, get_anthropic_client
from history import ConversationHistory

load_dotenv()


def run_openai_compatible(client, model, history):
    """Handles OpenAI, Groq, Cerebras — all use the same SDK."""
    stream = client.chat.completions.create(
        model=model,
        messages=history.get_messages(),
        stream=True,
    )
    full_response = ""
    for chunk in stream:
        if chunk.choices:
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="", flush=True)
                full_response += content
    return full_response


def run_anthropic(history):
    """Handles Anthropic Claude — uses its own SDK and stream interface."""
    import anthropic
    ac = get_anthropic_client()
    full_response = ""
    with ac.messages.stream(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=history.get_messages(),
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_response += text
    return full_response


def main():
    provider = os.getenv("PROVIDER", "groq").lower().strip()

    # Set up client only for non-anthropic providers
    if provider != "anthropic":
        client, model = get_client(provider)
        print(f"Chatbot ready ({provider} / {model})")
    else:
        client, model = None, None
        print("Chatbot ready (anthropic / claude-haiku-4-5-20251001)")

    history = ConversationHistory(max_tokens=4000)
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        history.add("user", user_input)
        print("Assistant: ", end="", flush=True)

        try:
            if provider == "anthropic":
                full_response = run_anthropic(history)
            else:
                full_response = run_openai_compatible(client, model, history)

            print()  # newline after streamed response
            history.add("assistant", full_response)
            history.trim_if_needed()

        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()