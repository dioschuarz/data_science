"""Define the States of the Graph."""
import operator
from typing import Annotated, List, TypedDict

from langchain_core.documents import Document


class OverallState(TypedDict):
    """
    Represents the overall state of the main graph.

    This state contains the input document contents, corresponding summaries,
    and a final summary.

    Attributes:
        contents (List[str]): The list of input document contents.
        token_max (int): The maximum number of tokens allowed.
        summaries (Annotated[list, operator.add]):
            The combined list of summaries generated from individual nodes.
        collapsed_summaries (List[Document]):
            The list of collapsed summaries as Document objects.
        final_summary (str):
            The final summary generated from the collapsed summaries.
    """
    contents: List[str]
    token_max: int
    summaries: Annotated[list, operator.add]
    collapsed_summaries: List[Document]
    final_summary: str


class SummaryState(TypedDict):
    """
    Represents the state of the node used to generate summaries.

    This state is mapped to all documents to generate individual summaries.

    Attributes:
        content (str): The content of the document to be summarized.
        token_max (int): The maximum number of tokens allowed.
    """
    content: str
    token_max: int
