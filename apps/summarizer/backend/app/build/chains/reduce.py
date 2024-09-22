"""Reduce size of chunks"""
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate

from backend.app.build.models import LLM


REDUCE_TEMPLATE = (
    """
    The following is a set of summaries:

    {docs}

    Take these and distill it into a final, consolidated summary
    using approximately {token_max} words, with a margin of 100 words
    for less or more.
    """
)

# Create the prompt chain
REDUCE_PROMPT = ChatPromptTemplate([("human", REDUCE_TEMPLATE)])
reduce_chain = REDUCE_PROMPT | LLM | StrOutputParser()
