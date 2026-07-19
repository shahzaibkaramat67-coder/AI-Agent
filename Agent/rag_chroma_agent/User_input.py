from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()

# model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
model = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_API_MODEL"))

embedding = HuggingFaceEmbeddings(model=os.getenv("EMBADDING_MODEL"))

vectorStore = Chroma(persist_directory="Chromadb", embedding_function=embedding)

retriever = vectorStore.as_retriever(
    search_type="mmr", search_kwargs={"fetch_k": 10, "k": 4, "lambda_mult": 0.7}
)

Template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
              you are a helpfull Ai Assistant use only the
               provided the context to answer the question 
               if the answer is not presnt in the context 
               say 'i could not find the answer in the document'
    
                 """,
        ),
        (
            "human",
            """
               content : {context},
               Question : {user_input}
                 """,
        ),
    ]
)


while True:
    user_input = input("Ask Question : ")
    if user_input == "Exit" or user_input.lower() == "exit":
        break
    docs = retriever.invoke(user_input)
    context = "\n\n".join([doc.page_content for doc in docs])

    final_prompt = Template.invoke({"context": context, "user_input": user_input})

    response = model.invoke(final_prompt)

    print("Response is :", response.content)
