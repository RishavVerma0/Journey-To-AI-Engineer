def chunk_text(text, size):
    if size <= 0:
        raise ValueError("size must be greater than 0")

    chunks = []
    index = 0

    while index < len(text):
        chunk = text[index:index + size]
        chunks.append(chunk)
        index += size

    return chunks

text = ("Hello World")

print(chunk_text(text, 2))