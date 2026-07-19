# from langchain.agents import create_agent
from mian import get_model
from memorySystem import memoryHendler
from langchain.messages import HumanMessage, AIMessage

model = get_model()


memory = memoryHendler()

print("the model is here", model)

# messages = [("assistant", "you are a help full asssistent in the domain of the law")]


def historyShow():
    print(memory)


# agent = create_agent(model=model, message=message)

while True:
    user_input = input("Ask Any Question About Law : ")
    if user_input == "Exit" or user_input == "exit":
        historyShow()
        break
    memory.append(HumanMessage(content=user_input))
    response = model.invoke(memory)
    result = response.content
    print("response", result)
    memory.append(AIMessage(content=result))
