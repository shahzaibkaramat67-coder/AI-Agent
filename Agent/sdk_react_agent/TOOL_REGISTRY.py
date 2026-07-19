"""
TOOL_REGISTRY.py — Gemini FunctionDeclaration objects for each tool.
"""

from google.genai import types

search_tool = types.FunctionDeclaration(
    name="search",
    description=(
        "Search the internet for factual, current, or external information. "
        "Use when the user asks about a person, company, product, technology, "
        "event, place, or any topic requiring web information. "
        "Returns titles, URLs, and page content snippets. "
        "Do NOT use for greetings, small talk, or questions answerable from context."
    ),
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "A concise search query.",
            }
        },
        "required": ["query"],
    },
)

research_tool = types.FunctionDeclaration(
    name="research",
    description=(
        "Perform deep analysis using sources previously obtained from search(). "
        "Use when the user asks for detailed explanations, comparisons, reports, "
        "or investigation. Always call search() first to populate sources. "
        "Do NOT call research without sources."
    ),
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The research question or topic.",
            },
        },
        "required": ["query"],
    },
)
