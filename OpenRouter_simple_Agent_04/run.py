from model import OpenRouterModel
from langchain_core.messages import AIMessage, HumanMessage
from memorySystem import SystemMemory

memory = SystemMemory()


def startChat():
    print(20*"=")
    print("Start The Chat")
    print(20*"=")

def showExitChat():
    print(20*"=")
    print("Enter The 'Exit' To End TEH Chat")
    print(20*"=")
showExitChat()
    
def endChat():
    print(20*"=")
    print("End The Chat")
    print(20*"=")
    
def start_Chating():
    startChat();
    while True:
        user_input = input("User : ")
        if "Exit" in user_input:
            endChat();
            break;
        memory.append(HumanMessage(content=user_input))
        response = OpenRouterModel(memory)
        print(response.content)
        memory.append(AIMessage(content=response.content))
