"""Define the edges of the LangGraph"""
from typing import Literal

from backend.app.build.graphs.states import OverallState
from backend.app.utils.functions import length_function


def should_collapse(
    state: OverallState,
) -> Literal["collapse_summaries", "generate_final_summary"]:
    """
    Determine whether to collapse the summaries or generate the final summary.

    This function acts as a conditional edge in the graph, deciding the next
    step based on the number of tokens in the collapsed summaries.

    Args:
        state (OverallState): The current state of the graph, containing the
                              collapsed summaries and the maximum
                              allowed tokens.

    Returns:
        Literal["collapse_summaries", "generate_final_summary"]:
            The next step in the process, either to collapse the summaries
            or to generate the final summary.
    """
    num_tokens = length_function(state["collapsed_summaries"])
    n_docs = len(state["collapsed_summaries"])
    if num_tokens > (state["token_max"]*n_docs):
        return "collapse_summaries"
    else:
        return "generate_final_summary"
