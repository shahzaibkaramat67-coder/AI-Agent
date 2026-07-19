from langchain_core.messages import  SystemMessage


def memoryMessage():
   return [
        SystemMessage(content="you are a help full assistent in law just law")
    ]