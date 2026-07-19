# from langchain_openai import ChatOpenAI
# from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()

def modelFunction(message):
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0.7,
        streaming=True
    )
    # responses = model.invoke(message)
    responses = model.stream(message)
    return responses