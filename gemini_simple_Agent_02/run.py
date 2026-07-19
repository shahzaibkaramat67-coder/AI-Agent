from langchain_core.messages import AIMessage, HumanMessage
from memorySyatem import memory
import model as model

message =  memory()

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
    
def Chat_syatem():
    startChat()
    while True:
        
        user_input = input("You : ")
        if user_input == "Exit":
            endChat()
            break;
        message.append(HumanMessage(content=user_input))
        responses = model.modelFunction(message)
        
        fullText = ""
        
        for chunk in responses:
             print(chunk.content, end="", flush=True)
             fullText += chunk.content
             message.append(AIMessage(content=fullText))
        print()

    





