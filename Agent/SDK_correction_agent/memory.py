class Memory:
    def __init__(self):
        self.messages = []

    def add_memory(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_memory(self):
        return self.messages[:]

    def get_text(self):
        return "\n".join(f"{m['role']} - {m['content']}" for m in self.get_memory())
