from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

import os

path = os.path.exists("D:\Agents\document\FYP_BlogWebsite_Final_Document.pdf")
print("path of the document : ", path)
document = PyPDFLoader("document/FYP_BlogWebsite_Final_Document.pdf")
loadDocument = document.load()

documentSpliter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)

chunks = documentSpliter.split_documents(loadDocument)


print("Chunk count : ", chunks)


embedding = HuggingFaceEmbeddings(model_name="zamanemon/text-embadding-0.1")

createDb = Chroma.from_documents(
    embedding=embedding,
    documents=chunks,
    persist_directory="Agent/RAG_02/Chromadb",
)


print("createDb._collection.count : ", createDb._collection.count())
