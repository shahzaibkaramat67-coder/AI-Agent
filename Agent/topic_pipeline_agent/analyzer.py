from Filnal_prompt import Templater
from model import llm


async def Analyzer(data):

    print(f"this is Analyzer funtion")

    system_prompt = """
you are a professional Analyzer, cleaner, remover unnecessary data from the input.

You are a strict JSON generator.

RULES:
- Return ONLY valid JSON
- NO markdown (no ```json)
- NO explanation
- NO extra text

Format:
{{
    "Approved": true,
    "Feedback": ""
}}

or

{{
    "Approved": false,
    "Feedback": "Explain what is missing."
}}

     


    """
    prompt = """
    Analysis of this data  : {data} 
    """
    final_prompt = Templater(system_prompt, prompt)
    result = final_prompt.invoke({"data": data})
    response = await llm(result)
    return response
