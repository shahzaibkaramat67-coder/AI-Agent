from pipliner import pipliner
from memory import Memory

memory = Memory()


if __name__ == "__main__":
    while True:
        user_input = input("Ask Anything : ")
        memory.add_memory({"role": "human", "content": user_input})
        stack = []
        stack.append({"type": "input", "content": user_input})

        if user_input == "Exit" or user_input.lower() == "exit":
            break

        response = pipliner(user_input, stack, memory.get_memory())
        print(response.content)
