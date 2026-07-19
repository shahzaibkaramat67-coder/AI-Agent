from langchain_core.messages import SystemMessage

system_prompt = "you are a expert coding again"
def memory():
   return [
        SystemMessage(content=system_prompt)
    ]