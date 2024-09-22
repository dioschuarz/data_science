"""Map themes in chunks"""
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate

from backend.app.build.models import LLM


MAP_TEMPLATE = (
    """
    The following is a set of documents:

    {docs}

    Based on this list of docs, please identify the main themes,
    considers usage of approximately {token_max} words,
    with a margin of 100 words for less or more, in your
    whole description.

    Helpful Answer:
    """
)

# Create the prompt chain
MAP_PROMPT = ChatPromptTemplate([("human", MAP_TEMPLATE)])
map_chain = MAP_PROMPT | LLM | StrOutputParser()
