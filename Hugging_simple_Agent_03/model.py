from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

def modelSetup(message):
    llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1",
    task="conversational",
    max_new_tokens=100,
    streaming=True,
    temperature=0.7
    )
    model = ChatHuggingFace(llm=llm)

    response = model.stream(message)
    return response
    

