from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
import os

load_dotenv()


# print(ChatGoogleGenerativeAI.list_model)

# model = ChatOpenAI(
#     base_url=os.getenv("OPENROUTER_API_KEY_URL"),
#     api_key=os.getenv("OPENROUTER_API_KEY"),
#     model="openrouter/free",
#     temperature=0.7,
# )

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


embedding = HuggingFaceEmbeddings(model="zamanemon/text-embadding-0.1")

vectorStore = Chroma(
    embedding_function=embedding, persist_directory="Agent/RAG_02/Chromadb"
)

retriver = vectorStore.as_retriever(
    search_type="mmr", search_kwargs={"fetch_k": 10, "k": 4, "lambda_mult": 0.7}
)


template = ChatPromptTemplate.from_messages(
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
        ("human", " User Question : {user_input} content : {context} "),
    ]
)


while True:
    user_input = input("Ask Question : ")
    if user_input == "Exit" or user_input == "exit":
        break
    docs = retriver.invoke(user_input)
    context = "\n".join([doc.page_content for doc in docs])

    final_prompt = template.invoke({"user_input": user_input, "context": context})

    response = model.invoke(final_prompt)

    print(response.content)
