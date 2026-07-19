from model import llm
from Filnal_prompt import Templater
from model import llm


async def outline_create(Topic):

    system_prompt = """
        you are a professioal article outliner writter
    """

    prompt = """ 
    create the outline of the topic
    topic : {Topic}
    may be you would get the previous result if Analyzer would not saticified 
    with you result then you have to improve the previous result 
    """
    final_prompt = Templater(system_prompt, prompt)
    message = final_prompt.invoke({"Topic": Topic})
    result = await llm(message)
    return result
