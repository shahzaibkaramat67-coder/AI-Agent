from Filnal_prompt import Templater
from model import llm


async def writter(topic_outline):
    system_prompt = """
    you are professional writter
    """

    prompt = """
     write the article 
    according to these outlines  : {topic_outline}
    """
    final_prompt = Templater(system_prompt, prompt)
    message = final_prompt.invoke({"topic_outline": topic_outline})
    result = await llm(message)
    return result
