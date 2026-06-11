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