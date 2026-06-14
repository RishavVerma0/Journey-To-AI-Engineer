# I am going to create a sample OpenAI API based system for testing purposes
#This system will work with OpenAI, Gemini, Groq, Openrouter, Cerebras... etc


from openai import OpenAI

api_key = "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"
base_url = "https://api.anthropic.com/v1/"
model = "claude-sonnet-4-5"

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
