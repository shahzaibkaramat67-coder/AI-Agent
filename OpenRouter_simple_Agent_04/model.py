from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def OpenRouterModel(memory):
    llm = ChatOpenAI(
      base_url=os.getenv("OPENROUTER_API_KEY_URL"),
      api_key=os.getenv("OPENROUTER_API_KEY"),
      max_tokens=200,
      model="qwen/qwen3.7-max"
    #   model="openai/gpt-4o"
    #   model="anthropic/claude-3.7-sonnet"
    #   model="google/gemini-2.5-pro"
    #   model="meta-llama/llama-3.3-70b-instruct"
    #   model="mistralai/mistral-large"
    #   model="qwen/qwen-2.5-72b"
       )

    response = llm.invoke(memory)
    return response


