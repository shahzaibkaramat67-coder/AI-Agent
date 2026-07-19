"""
tool_schema.py — Assembles the Gemini Tool object from registered declarations.
"""

from google.genai import types
from TOOL_REGISTRY import search_tool, research_tool


def get_tools() -> list[types.Tool]:
    return [types.Tool(function_declarations=[search_tool, research_tool])]
