from planner import planner
from memory import Memory
from executer import execute
from tools import search, resaerch
from evaluate import evaluator
from final_answer import final_result
import json


def pipliner(query, stack, memory):

    max_itrate = 5
    for step in range(max_itrate):
        plan = planner(query, memory, stack)

        plan_result = json.loads(plan)

        executor = execute(plan_result)

        memory.add_memory({"role": plan_result, "content": executor})
        stack["plan_result"] = plan_result
        stack["executor"] = executor

        evaluate = evaluator(executor)

        if evaluate["False"]:
            step += 1
        else:
            result = final_result(query, memory, stack)

    return result

    # Tool = plan_result["tool"]
    # if Tool == "search":
    #     search_result = search(plan_result["tool_input"])
    #     memory.add_memory(Tool, search_result)
    #     stack.append({"Tool": Tool, "Tool_output": search_result})
    # elif Tool == "research":
    #     research_result = resaerch(plan_result["tool_input"])
    #     memory.add_memory(Tool, research_result)
    #     stack.append({"Tool": Tool, "Tool_output": research_result})
    # elif Tool == "none":
    #     memory.add_memory(Tool, "no tool use")
    #     stack.append({"Tool": Tool, "Tool_output": "no output comes"})
