from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def modelfunction(message):
       model = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
        )
       response = model.invoke(message);
       return response


