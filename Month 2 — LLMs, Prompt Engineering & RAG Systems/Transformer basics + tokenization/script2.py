from openai import OpenAI, RateLimitError
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

try:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a concise assistant."},
            {"role": "user", "content": "Explain attention in one sentence."}
        ],
        temperature=1.7
    )

    print("Reply:", response.choices[0].message.content)

    if response.usage:
        print("Input tokens :", response.usage.prompt_tokens)
        print("Output tokens:", response.usage.completion_tokens)
        print("Total tokens :", response.usage.total_tokens)

except RateLimitError as e:
    print("Rate limit or quota issue:")
    print(e)

except Exception as e:
    print("Error:", e)