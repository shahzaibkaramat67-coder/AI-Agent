"""
entrypoint.py — CLI entry point.

One Memory instance is created here and passed through the whole stack
so every component shares a single source of truth.
"""

from __future__ import annotations

from memory import Memory
from Agent import run_agent


def entry_point() -> None:
    memory = Memory()
    print("AI Agent ready. Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit", "bye"}:
            print("Goodbye!")
            break

        memory.add_memory("human", user_input)
        run_agent(memory)
