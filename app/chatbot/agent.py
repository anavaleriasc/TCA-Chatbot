from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

  

def get_agent():

   load_dotenv()
   api_key = os.getenv("GOOGLE_API_KEY")

   agent = ChatGoogleGenerativeAI(
      model="gemini-2.5-flash-lite",
      api_key=api_key,
   )
   return agent

