from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# from tools import search, resaerch
import os

# API_KEY = os.getenv("GEMINI_API_KEY")
model = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_API_MODEL"))
print("model", model)

# system_message = """

# You are a professioanl saerch agent


# take the query form the user and saerch on it
# and return result

# you have the tools
# you can use any tools form them for the take but
# you must carefull about it and follow the ruls

# Ruls:
# - analsis the user query
# - take the right tool for the query
# - find the best data
# - select only most ralivent result according to the user query
# - after search get most ralivent nearable efficient result for then next agent

# """


load_dotenv()


agent = create_agent(model=model)
