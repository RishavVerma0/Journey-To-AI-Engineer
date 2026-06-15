from openai import OpenAI
from dotenv import load_dotenv

import os

load_dotenv()

client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

stream = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": "Tell me a 3-line story about a robot."}],
    stream=True,
    stream_options={"include_usage": True}
)

full_reply = ""
chunk_count = 0


for chunk in stream:
    delta= chunk.choices[0].delta.content if chunk.choices else None
    if delta:
        print(delta, end="", flush=True)
        full_reply += delta
        chunk_count += 1
    if chunk.usage:
        print(f"\n\n Total Tokens: {chunk.usage.total_tokens}")

print(f"\nChunks received: {chunk_count}")
print(f"\nFull reply length: {len(full_reply)} chars")