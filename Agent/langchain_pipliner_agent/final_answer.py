from agent import agent


def final_result(query, memory, stack):

    system_prompt = f"""
    
    you will get a last result you just write the final
    result 


    query : {query}
    memory : {memory}
    stack : {stack}
    
    """

    response = agent.invoke(system_prompt)
    return response.content
