from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
model="llama-3.1-8b-instant"
client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

prompt = input("\nPlease Enter Your Prompt >> ")

while prompt.strip().lower() != "exit":

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content" : "You are a helpful Assistant."},
            {"role": "user", "content" : prompt}
        ],stream=True
    )
    print("\nAssistant >> ", end="", flush=True)

    for chunk in response:

        content = chunk.choices[0].delta.content

        if content:

            print(content, end="", flush=True)

    print("\n")
    
    prompt = input("\nPlease Enter Your Prompt >> ")