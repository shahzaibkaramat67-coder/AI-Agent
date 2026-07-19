from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()


async def llm(prompt):
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_API_MODEL_FLASH"),
    )
    response = await llm.ainvoke(prompt)
    return response.content
