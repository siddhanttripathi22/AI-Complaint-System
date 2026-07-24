"""
This file wires the nodes into an actual LangGraph.

The graph is the "recipe" that says which step runs after which.
There is one decision point: if the input text is empty, we skip all the
AI work and go straight to the end.

    check_input --(ok)--> extract --> classify_risk --> check_completeness --> summarize --> recommend_capa --> END
         |
       (empty) --------------------------------------------------------------------------------------------> END
"""
from langgraph.graph import StateGraph, END

from app.agent import nodes
from app.agent.state import ComplaintState


def _route_after_input(state: ComplaintState) -> str:
    """Conditional edge: decide where to go after the input check."""
    if state.get("error"):
        return "stop"      # bad input -> jump to END
    return "continue"      # good input -> carry on to extraction


def build_graph():
    graph = StateGraph(ComplaintState)

    # Register each node under a name.
    graph.add_node("check_input", nodes.check_input)
    graph.add_node("extract", nodes.extract)
    graph.add_node("classify_risk", nodes.classify_risk)
    graph.add_node("check_completeness", nodes.check_completeness)
    graph.add_node("summarize", nodes.summarize)
    graph.add_node("recommend_capa", nodes.recommend_capa)

    # Where does the graph start?
    graph.set_entry_point("check_input")

    # Branch based on whether the input was valid.
    graph.add_conditional_edges(
        "check_input",
        _route_after_input,
        {"continue": "extract", "stop": END},
    )

    # The straight-line happy path.
    graph.add_edge("extract", "classify_risk")
    graph.add_edge("classify_risk", "check_completeness")
    graph.add_edge("check_completeness", "summarize")
    graph.add_edge("summarize", "recommend_capa")
    graph.add_edge("recommend_capa", END)

    return graph.compile()


# Compile once at import time and reuse for every request.
complaint_agent = build_graph()


def run_agent(raw_text: str) -> ComplaintState:
    """Convenience wrapper the API calls with the complaint text."""
    return complaint_agent.invoke({"raw_text": raw_text})
