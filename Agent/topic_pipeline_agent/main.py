from pipeline import pipeline
import asyncio

if __name__ == "__main__":
    while True:
        user_input = input("Write Topic : ")
        if user_input == "Exit" or user_input == "exit":
            break
        # Piplinig(user_input)
        # result = asyncio.run(pipeline(topic))
        result = asyncio.run(pipeline(user_input))
        print("Final Result : \n", result)
