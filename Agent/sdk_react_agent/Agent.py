"""
Agent.py — ReAct agent loop.

Each call to `run_agent(memory)` runs one full reasoning cycle for
the current user turn:

  Reason → Act (tool) → Observe → Reason → ... → Final Answer

The loop exits when:
  • The model returns a text response (no tool call)  → print answer
  • MAX_STEPS is reached without a final answer       → warn and exit
"""

from __future__ import annotations

from rich import print as rprint
from memory import Memory
from model import call_model
from Tools import search, research

MAX_STEPS = 3


def _emit(kind: str, message: str) -> None:
    rprint(f"[bold cyan][{kind}][/bold cyan] {message}")


def run_agent(memory: Memory) -> str | None:
    """
    Run the ReAct loop against `memory` (which must already contain the
    latest human turn).

    Returns the final text answer, or None if the loop exhausted MAX_STEPS.
    """
    for step in range(1, MAX_STEPS + 1):
        _emit("STEP", f"{step}/{MAX_STEPS}")

        part = call_model(memory)

        # ── Tool call ────────────────────────────────────────────────────
        if part.function_call:
            tool_name = part.function_call.name
            tool_args = dict(part.function_call.args)
            _emit("TOOL", f"Calling `{tool_name}` with args: {tool_args}")

            if tool_name == "search":
                results = search(query=tool_args["query"], emit=_emit)

                if not results:
                    observation = "Search returned no results."
                else:
                    observation = "\n".join(
                        f"Title: {r['title']}\nURL: {r['href']}\nContent: {r['content']}"
                        for r in results
                    )
                    # Cache raw results so `research` can use them later
                    memory.add_memory("search_tool_result", results)

                _emit("OBSERVE", f"{len(results)} result(s) fetched")
                memory.add_memory("search_tool_result_text", observation)

                # Feed the observation back as a user turn so the model sees it
                memory.add_memory(
                    "user",
                    f"[SEARCH RESULT for '{tool_args['query']}']\n{observation}",
                )

            elif tool_name == "research":
                # Retrieve the cached raw search results
                sources: list[dict] = memory.get_memory("search_tool_result") or []

                if not sources:
                    observation = (
                        "research() was called but no search results are available. "
                        "Please call search() first."
                    )
                    _emit("WARN", observation)
                else:
                    observation = research(
                        query=tool_args["query"],
                        sources=sources,
                        emit=_emit,
                    )
                    memory.add_memory("research_tool_result", observation)

                memory.add_memory(
                    "user",
                    f"[RESEARCH RESULT for '{tool_args['query']}']\n{observation}",
                )

            else:
                _emit("WARN", f"Unknown tool: {tool_name!r} — skipping")

            continue  # go back to the top → model reasons again

        # ── Final text answer ────────────────────────────────────────────
        answer = (part.text or "").strip()
        if answer:
            rprint(f"\n[bold green]ANSWER:[/bold green] {answer}\n")
            memory.add_memory("assistant", answer)
            return answer

        # Model returned neither a tool call nor text — shouldn't happen
        _emit("WARN", "Model returned an empty part. Retrying…")

    _emit("WARN", f"Reached MAX_STEPS ({MAX_STEPS}) without a final answer.")
    return None
