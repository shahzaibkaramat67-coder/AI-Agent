from memory import Memory
from Agent import run_agent

memory = Memory()


def enteryPoint():

    while True:

        user_input = input("\nAsk Question : ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        memory.add_memory("human", user_input)

        print("\n[MEMORY]")
        print(memory.get_memory())

        try:
            run_agent()

        except Exception as e:
            print(f"\n[ERROR] {e}")
