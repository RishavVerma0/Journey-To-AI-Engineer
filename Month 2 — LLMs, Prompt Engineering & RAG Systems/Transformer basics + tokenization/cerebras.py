# I am going to create a sample OpenAI API based system for testing purposes
#This system will work with OpenAI, Gemini, Groq, Openrouter, Cerebras... etc


from openai import OpenAI

api_key = ""
base_url = "https://api.cerebras.ai/v1"
model = "gpt-oss-120b"

client = OpenAI(api_key=api_key, base_url=base_url)

prompt = input("\n User >>")

while prompt.strip().lower() != "exit":

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content" : "You are a helpful Assistant."},
            {"role": "user", "content" : prompt}
        ]
    )
    print("Response: ", response.choices[0].message.content)


    prompt = input("\n User >>") 
