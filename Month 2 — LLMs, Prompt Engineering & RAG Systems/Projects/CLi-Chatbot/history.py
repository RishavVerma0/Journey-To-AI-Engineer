class ConversationHistory:
    def __init__(self, max_tokens: int = 4000, system_prompt: str = "You are a helpful assistant."):
        self.system_prompt = system_prompt
        self.messages = []
        self.max_tokens = max_tokens

    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def get_messages(self):
        """Returns full message list including system prompt."""
        return [{"role": "system", "content": self.system_prompt}] + self.messages

    def trim_if_needed(self):
        """Remove oldest messages if token estimate exceeds limit."""
        while self.token_estimate() > self.max_tokens and len(self.messages) > 2:
            self.messages.pop(0)

    def token_estimate(self) -> int:
        """Rough estimate: 1 token ≈ 4 characters."""
        total_chars = sum(len(m["content"]) for m in self.messages)
        return total_chars // 4