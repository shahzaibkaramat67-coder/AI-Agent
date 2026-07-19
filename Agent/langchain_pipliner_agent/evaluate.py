from agent import agent


def evaluator(evaluator):
    system_prompt = f"""
    
    you are professioanl evaluator 
    evaluate the give data and return if you saticified the True
    else Fales
    

    evaluator :{evaluator}
    
    
    retuen json 
    
    {{
          "evaluator": "",
         
    }}

    """

    response = agent.invoke(system_prompt)
    return response.content
