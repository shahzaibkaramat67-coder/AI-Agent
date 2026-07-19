from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma

import os

load_dotenv()

pdf = PyPDFLoader("document/FYP_BlogWebsite_Final_Document.pdf")

document = pdf.load()

textSplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

Chunks = textSplitter.split_documents(documents=document)


embadding = HuggingFaceEmbeddings(model=os.getenv("EMBADDING_MODEL"))

createDB = Chroma.from_documents(
    documents=Chunks, embedding=embadding, persist_directory="Chromadb"
)
