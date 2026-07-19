from agent import agent
from tools import search, resaerch


def execute(plan):
    Tool = plan.get("tool")
    Tool_input = plan.get("tool_input")
    if Tool == "search":
        return search(Tool_input)

    elif Tool == "research":
        return resaerch(Tool_input)

    elif Tool == "none":
        return None
