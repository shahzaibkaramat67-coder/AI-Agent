from google.genai import types
from Tools import search, research

search_tool = types.FunctionDeclaration(
    name="search",
    description="""
    Search the internet for factual, current, or external information.

Use this tool when:
- The answer requires web information.
- The user asks about a person, company, product, technology, event, place, or topic.
- The user asks for recent or up-to-date information.
- Sources are needed before deeper analysis.

Do NOT use for:
- Greetings
- Small talk
- Casual conversation
- Thank-you messages
- Questions answerable without external information

This tool returns titles, URLs, and snippets only.
    """,
    parameters={
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"],
    },
)


research_tool = types.FunctionDeclaration(
    name="research",
    description="""
    Perform deep research and analysis using sources.

Use this tool when:
- The user asks for detailed explanations.
- The user asks for comparisons.
- The user asks for research, investigation, reports, or analysis.
- Search results alone are insufficient.

Requirements:
- Search should normally be used first.
- Research requires sources from search().
- Use research after gathering relevant search results.

Do NOT use for:
- Greetings
- Small talk
- Simple factual questions
- Questions that can be answered directly from search results

This tool reads and analyzes sources and produces detailed findings.
    """,
    parameters={
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "sources": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["query", "sources"],
    },
)


# TOOL_REGISTRY = {
#     "search": {
#         "function": search,
#         "description": "Search the web for information",
#         "parameters": {
#             "type": "object",
#             "properties": {"query": {"type": "string", "description": "Search query"}},
#             "required": ["query"],
#         },
#     },
#     "research": {
#         "function": research,
#         "description": "Research a topic deeply",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "query": {"type": "string", "description": "Research topic"}
#             },
#             "required": ["query"],
#         },
#     },
# }
