from Filnal_prompt import Templater
from model import llm


async def Editer(Edit_article):

    system_prompt = """
    you are a professioanl editer
    """

    prompt = """
    edit the article 
    and  improve grammer, readability, formatting, and clearity
    
    Article : {Edit_article}
    
    """

    final_prompt = Templater(system_prompt, prompt)
    message = final_prompt.invoke({"Edit_article": Edit_article})
    result = await llm(message)
    return result
