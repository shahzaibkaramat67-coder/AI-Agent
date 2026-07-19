"""
model.py — Thin wrapper around the Gemini API.

Returns the first Part of the first candidate, which is either:
  - A text Part  (part.text is set, part.function_call is None)
  - A tool Part  (part.function_call is set, part.text is None/empty)
"""

from __future__ import annotations

import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from tool_schema import get_tools
from memory import Memory

load_dotenv()

_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

SYSTEM_INSTRUCTION = """
You are a helpful AI agent with access to two tools:

1. search(query)
   • Find relevant web information: facts, current events, people, companies,
     products, technologies, locations, etc.
   • Returns titles, URLs, and page content snippets.
   • Use BEFORE research when external information is needed.

2. research(query)
   • Deep analysis using sources you already retrieved with search().
   • Use for detailed explanations, comparisons, reports, investigations.
   • ONLY call this after search() has been used in this conversation.

Workflow:
  a. If external information is needed → call search().
  b. If deeper analysis is needed after search → call research().
  c. Once you have enough information → answer the user directly (no tool call).

Do NOT call any tool for:
  • Greetings, introductions, small talk ("Hi", "How are you?", "Thanks")
  • Questions answerable from the existing conversation context

When you respond without a tool, write your final answer directly to the user.
""".strip()


def call_model(memory: Memory) -> types.Part:
    """
    Send the current conversation to Gemini and return the first Part.

    The returned Part has either `.text` (final answer) or `.function_call`
    (tool invocation) set — never both.
    """
    contents = memory.get_contents()

    response = _client.models.generate_content(
        model=os.environ["GEMINI_API_MODEL"],
        contents=contents,
        config=types.GenerateContentConfig(
            tools=get_tools(),
            system_instruction=SYSTEM_INSTRUCTION,
        ),
    )

    # Gemini may return multiple parts; the first one carries the action.
    part = response.candidates[0].content.parts[0]
    return part
