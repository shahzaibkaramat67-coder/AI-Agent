"""
memory.py — Conversation memory that formats correctly for Gemini's `contents` API.

Gemini expects `contents` as a list of dicts:
    [{"role": "user", "parts": [{"text": "..."}]}, ...]

Supported roles: "user" | "model"
We map:
    "human"              → "user"
    "assistant"          → "model"
    "search_tool_result" → stored as metadata (not sent to model directly)
    "research_tool_result" → stored as metadata (not sent to model directly)
    tool results are injected back as a "user" turn so the model can see them.
"""

from typing import Any

ROLE_MAP = {
    "human": "user",
    "assistant": "model",
    "user": "user",
    "model": "model",
}

# Roles that represent tool output — injected as "user" turns in the transcript
TOOL_ROLES = {"search_tool_result", "research_tool_result"}


class Memory:
    def __init__(self):
        # Each entry: {"role": str, "content": Any}
        self._messages: list[dict] = []

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def add_message(self, role: str, content: Any) -> None:
        """Append a message with an explicit role."""
        self._messages.append({"role": role, "content": content})

    # Convenience aliases used throughout the codebase
    def add_memory(self, role: str, content: Any) -> None:
        self.add_message(role, content)

    # ------------------------------------------------------------------
    # Read — raw
    # ------------------------------------------------------------------

    def get_memory(self, role: str | None = None) -> list[dict] | Any | None:
        """
        No argument  → return a shallow copy of all messages.
        With a role  → return the *content* of the last message with that role,
                       or None if not found.
        """
        if role is None:
            return self._messages[:]
        for msg in reversed(self._messages):
            if msg["role"] == role:
                return msg["content"]
        return None

    # ------------------------------------------------------------------
    # Read — Gemini-formatted
    # ------------------------------------------------------------------

    def get_contents(self) -> list[dict]:
        """
        Return the conversation formatted for Gemini's `contents` parameter.

        Rules:
        - "human" / "user"          → role "user"
        - "assistant" / "model"     → role "model"
        - tool result roles         → role "user" with a labelled prefix
        - unknown roles             → role "user" (safe fallback)
        - Consecutive turns of the same role are merged (Gemini requires
          strict user/model alternation).
        """
        contents: list[dict] = []

        for msg in self._messages:
            role = msg["role"]
            content = msg["content"]

            if role in TOOL_ROLES:
                label = role.replace("_", " ").upper()
                text = (
                    f"[{label}]\n{content}"
                    if isinstance(content, str)
                    else f"[{label}]\n{content!r}"
                )
                gemini_role = "user"
            else:
                gemini_role = ROLE_MAP.get(role, "user")
                text = content if isinstance(content, str) else str(content)

            # Merge consecutive same-role turns
            if contents and contents[-1]["role"] == gemini_role:
                contents[-1]["parts"][0]["text"] += "\n\n" + text
            else:
                contents.append({"role": gemini_role, "parts": [{"text": text}]})

        return contents

    # ------------------------------------------------------------------
    # Misc
    # ------------------------------------------------------------------

    def clear(self) -> None:
        self._messages.clear()

    def __repr__(self) -> str:
        return f"Memory({len(self._messages)} messages)"
