from langchain_core.messages import SystemMessage


def SystemMemory():
    return [
        SystemMessage(content="you are a angry guy")
    ]