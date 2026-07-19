import simple_Agent as model
from langchain_core.messages import HumanMessage, AIMessage
from memory import memoryMessage

# Load memory
message = memoryMessage()

print("message =", message)


def welcome():
    print("Welcome to AI Agent")


def chat_System():

    welcome()

    print(10 * "=", "write exit to exit chat", 10 * "=")

    while True:

        user_input = input("You : ")

        if user_input == "exit":
            break

        # Store human message
        message.append(
            HumanMessage(content=user_input)
        )

        # Get AI response
        response = model.modelfunction(message)

        # Store AI response
        message.append(
            AIMessage(content=response.content)
        )

        # Print response
        print(response.content)


# Start app from chat system
