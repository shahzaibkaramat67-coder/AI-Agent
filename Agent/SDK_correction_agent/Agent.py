from model import modelfunction
from memory import Memory

# from model import client
from dotenv import load_dotenv
from Tools import search, research
from rich import print
import json

import os

load_dotenv()

memory = Memory()
print("memory", memory)


def emit(type, message):
    print(f"[{type}] {message}")


import re
import json

# def safe_json_parse(text):
#     text = text.strip()

#     # remove markdown fences
#     text = re.sub(r"```json|```", "", text)

#     # try parsing
#     return json.loads(text)


def run_agent():

    while True:

        response = modelfunction(memory)
        print("response for the text or function call", response)
        print("response for the text or without function call", response.text)
        Tool = response.function_call
        print("TOOL", Tool)

        if Tool:
            if Tool.name == "search":
                search_result = search(Tool.args["query"], emit=emit)
                print("search_result", search_result)
                search_final_result = "\n".join(
                    f"title : {r['title']} \n URL : {r['href']} \n Content : {r['content']}"
                    for r in search_result
                )
                print("search_final_result", search_final_result)
                memory.add_memory("search_tool_result", search_final_result)
                print(
                    "memory show after update the search result : ", memory.get_memory()
                )
                continue
                # ✅ Fixed
            elif Tool.name == "research":
                source_memory = memory.get_memory("search_tool_result")
                research_result = research(
                    query=Tool.args["query"], sources=source_memory, emit=emit
                )
                memory.add_memory("research_tool_result", research_result)
        else:
            print(response.text)


# from model import modelfunction
# from memory import Memory
# from dotenv import load_dotenv
# from Tools import search, research
# import json, os

# load_dotenv()


# def emit(type, message):
#     print(f"[{type}] {message}")


# # def clean_json(text: str) -> str:
# #     text = text.strip()
# #     text = re.sub(r"^```json\s*", "", text)
# #     text = re.sub(r"^```\s*", "", text)
# #     text = re.sub(r"```$", "", text)
# #     return text.strip()


# def enteryPoint():
#     memory = Memory()
#     MAX_STEPS = 10

#     while True:
#         user_input = input("\nAsk Question: ").strip()
#         if user_input.lower() == "exit":
#             break

#         memory.add_memory("human", user_input)
#         step = 0

#         # ✅ Inner ReAct loop — Reason → Act → Observe → Repeat
#         while step < MAX_STEPS:
#             step += 1
#             raw = modelfunction(memory)

#             try:
#                 jsonResponse = json.loads(raw)
#             except json.JSONDecodeError:
#                 print("❌ Model returned invalid JSON:", raw)
#                 break

#             tool = jsonResponse.get("tool", "none")

#             if tool == "none":
#                 answer = jsonResponse.get("answer", "I don't know.")
#                 print(f"\n✅ FINAL ANSWER: {answer}")
#                 memory.add_memory("assistant", answer)
#                 break

#             elif tool == "search":
#                 result = search(jsonResponse["args"]["query"], emit=emit)
#                 memory.add_memory("tool", f"[SEARCH RESULT]\n{result}")

#             elif tool == "research":
#                 result = research(jsonResponse["args"]["query"], emit=emit)
#                 memory.add_memory("tool", f"[RESEARCH RESULT]\n{result}")

#             else:
#                 print(f"❌ Unknown tool: {tool}")
#                 break
#         else:
#             print("⚠️ Max steps reached without final answer.")
