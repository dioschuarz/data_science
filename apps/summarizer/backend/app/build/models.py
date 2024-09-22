"""Define models used in this app"""
from langchain_google_genai import (ChatGoogleGenerativeAI,
                                    GoogleGenerativeAIEmbeddings)
import tiktoken

from backend.app.utils.config import GOOGLE_API_KEY


# Initialize the language model
LLM = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",
                             api_key=GOOGLE_API_KEY,
                             temperature=0)

# Initialize the embedding model
EMBEDDING = GoogleGenerativeAIEmbeddings(model="models/embedding-001",
                                         google_api_key=GOOGLE_API_KEY)

# Get the encoding for the GPT-2 model
ENCODING = tiktoken.get_encoding("gpt2")
