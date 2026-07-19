# from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()


def get_model():
    model = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_API_MODEL"))
    return model


# model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
