from agent import agent


def planner(query, stack, memory):
    planing_agent_prompt = f"""
    
      you are a professioanl planner agent 
    just build a structure plan to do any task
    
  

Return ONLY JSON:

{{
    "tool": "",
    "tool_input": "",
    "reason": ""
}}

    Query : {query}
    stack : {stack}
    memory : {memory}
    
    """

    response = agent.invoke(planing_agent_prompt)
    return response.content
