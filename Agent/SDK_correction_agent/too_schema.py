from TOOL_REGISTRY import research_tool, search_tool
from google.genai import types


def get_Tools():
    return [types.Tool(function_declarations=[search_tool, research_tool])]
