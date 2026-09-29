import os
from importlib.metadata import version

from dotenv import load_dotenv

load_dotenv()

from langchain_core import __version__ as core_version
from langchain_google_genai import ChatGoogleGenerativeAI


def main():
    print("Hello from complete-rag!")

    print(f"LangChain Core: {core_version}")
    print(f"LangGraph: {version('langgraph')}")

    print(f"Gemini key loaded: {bool(os.getenv('GOOGLE_API_KEY'))}")

    print("Initializing Chat Model...")

    gemini_model = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0
    )

    print("Gemini model initialized successfully.")

    response = gemini_model.invoke(
        "Explain RAG in one sentence."
    )

    print("\nGemini response:")
    print(response.content)


if __name__ == "__main__":
    main()