"""Define the Nodes of the LangGraph."""
from langchain.chains.combine_documents.reduce import (
    split_list_of_docs
)
from langchain_core.documents import Document
from langchain.text_splitter import TokenTextSplitter
from langgraph.constants import Send

# from backend.app.build.chains.map import map_chain
from backend.app.build.chains.reduce import reduce_chain
from backend.app.build.graphs.states import OverallState, SummaryState
from backend.app.build.models import ENCODING
from backend.app.utils.functions import length_function


def collect_summaries(state: OverallState) -> dict:
    """
    Collect summaries from the state.

    Args:
        state (OverallState): The current state containing summaries
                              and token_max.

    Returns:
        dict: A dictionary with collapsed summaries and token_max.
    """
    print("COLLECT_SUMMARIES")
    summaries = []
    for summary in state["summaries"]:
        tokens = ENCODING.encode(summary)
        print("Used:", len(tokens),
              "Expected:", state["token_max"])
        summaries.append(Document(summary))
    return {
        "collapsed_summaries": summaries,
        "token_max": state["token_max"]
    }


async def collapse_summaries(state: OverallState) -> dict:
    """
    Collapse summaries into smaller chunks if they exceed the token limit.

    Args:
        state (OverallState): The current state containing collapsed summaries
                              and token_max.

    Returns:
        dict: A dictionary with updated collapsed summaries and token_max.
    """
    doc_lists = split_list_of_docs(
        state["collapsed_summaries"],
        length_function,
        state["token_max"]
    )
    print("COLLAPSE_SUMMARIES")
    for doc in doc_lists:
        tokens = ENCODING.encode(doc[0].page_content)
        print("Used:", len(tokens),
              "Expected:", state["token_max"])
    results = []
    for doc_list in doc_lists:
        req = {"docs": doc_list[0],
               "token_max": state["token_max"]}
        results.append(
            Document(await reduce_chain.ainvoke(req))
            )

    return {
        "collapsed_summaries": results,
        "token_max": state["token_max"]
    }


async def generate_summary(state: SummaryState) -> dict:
    """
    Generate a summary for a given document.

    Args:
        state (SummaryState): The current state containing content
                              and token_max.

    Returns:
        dict: A dictionary with generated summaries and token_max.
    """
    print("GENERATE_SUMMARY")
    text_splitter = TokenTextSplitter(chunk_size=state["token_max"]*4,
                                      chunk_overlap=100)
    raw_doc = Document(state["content"])
    docs = text_splitter.split_documents([raw_doc])
    response = []
    for doc in docs:
        req = {"docs": doc,
               "token_max": state["token_max"]}
        tokens = list(range(-1, state['token_max']))
        while len(tokens) > state["token_max"]:
            text = await reduce_chain.ainvoke(req)
            tokens = ENCODING.encode(text)
        response.append(text)
        print("Used:", len(tokens),
              "Expected:", state["token_max"])
    return {
        "summaries": response,
        "token_max": state["token_max"]
    }


async def generate_final_summary(state: OverallState) -> dict:
    """
    Generate the final summary from collapsed summaries.

    Args:
        state (OverallState): The current state containing collapsed summaries
                              and token_max.

    Returns:
        dict: A dictionary with the final summary and token_max.
    """
    print("GENERATE_FINAL_SUMMARY")
    for doc in state["collapsed_summaries"]:
        tokens = ENCODING.encode(doc.page_content)
        print("Used:", len(tokens),
              "Expected:", state["token_max"])
    req = {"docs": state["collapsed_summaries"],
           "token_max": state["token_max"]}
    response = await reduce_chain.ainvoke(req)
    return {
        "final_summary": response,
        "token_max": state["token_max"]
    }


def map_summaries(state: OverallState) -> list:
    """
    Define the logic to map out over the documents.

    Args:
        state (OverallState): The current state containing contents
                              and token_max.

    Returns:
        list: A list of `Send` objects with the name of a node in the graph
              and the state to send to that node.
    """
    return [
        Send(
            "generate_summary",
            {
                "content": content,
                "token_max": state["token_max"]
            }
        ) for content in state["contents"]
    ]
