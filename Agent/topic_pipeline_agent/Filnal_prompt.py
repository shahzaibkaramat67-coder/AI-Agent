from langchain_core.prompts import ChatPromptTemplate


def Templater(system_prompt, prompt):

    template = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("human", prompt)]
    )

    return template
