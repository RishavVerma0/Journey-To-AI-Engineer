import tiktoken

enc = tiktoken.encoding_for_model("gpt-4")

def analyze(text):
    tokens = enc.encode(text)
    print(f"\nText   : {text}")
    print(f"Tokens : {tokens}")
    print(f"Count  : {len(tokens)}")
    decoded = [enc.decode([t]) for t in tokens]
    print(f"Words  : {decoded}")

analyze("Hello, my name is Claude.")
analyze("ChatGPT is amazing!")
analyze("def fibonacci(n): return n")
analyze("नमस्ते")       # Hindi
analyze("1 + 1 = 2")

def estimate_cost(text, model="gpt-4o-mini"):
    tokens = enc.encode(text)
    # gpt-4o-mini: $0.00015 per 1K input tokens
    cost = (len(tokens) / 1000) * 0.00015
    print(f"Tokens: {len(tokens)}, Est. cost: ${cost:.6f}")

estimate_cost("Write me a poem about Python programming.")