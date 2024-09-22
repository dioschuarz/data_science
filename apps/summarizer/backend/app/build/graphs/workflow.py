"""Build LangGraph workflow"""
from langgraph.graph import END, START, StateGraph

from backend.app.build.graphs.edges import should_collapse
from backend.app.build.graphs.nodes import (collapse_summaries,
                                            collect_summaries,
                                            generate_final_summary,
                                            generate_summary,
                                            map_summaries)
from backend.app.build.graphs.states import OverallState


# Construct the graph
# Nodes:
graph = StateGraph(OverallState)
graph.add_node("generate_summary", generate_summary)
graph.add_node("collect_summaries", collect_summaries)
graph.add_node("collapse_summaries", collapse_summaries)
graph.add_node("generate_final_summary", generate_final_summary)

# Edges:
graph.add_conditional_edges(START, map_summaries, ["generate_summary"])
graph.add_edge("generate_summary", "collect_summaries")
graph.add_conditional_edges("collect_summaries", should_collapse)
graph.add_conditional_edges("collapse_summaries", should_collapse)
graph.add_edge("generate_final_summary", END)

SUMMARIZER_GRAPH = graph.compile()
