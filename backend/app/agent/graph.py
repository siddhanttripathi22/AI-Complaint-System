from langgraph.graph import StateGraph, END

from app.agent import nodes
from app.agent.state import ComplaintState


def _route_after_input(state: ComplaintState) -> str:
    """Conditional edge: decide where to go after the input check."""
    if state.get("error"):
        return "stop"      
    return "continue"      


def build_graph():
    graph = StateGraph(ComplaintState)

    
    graph.add_node("check_input", nodes.check_input)
    graph.add_node("extract", nodes.extract)
    graph.add_node("classify_risk", nodes.classify_risk)
    graph.add_node("check_completeness", nodes.check_completeness)
    graph.add_node("summarize", nodes.summarize)

    
    graph.set_entry_point("check_input")

    
    graph.add_conditional_edges(
        "check_input",
        _route_after_input,
        {"continue": "extract", "stop": END},
    )

   
    graph.add_edge("extract", "classify_risk")
    graph.add_edge("classify_risk", "check_completeness")
    graph.add_edge("check_completeness", "summarize")
    graph.add_edge("summarize", END)

    return graph.compile()



complaint_agent = build_graph()


def run_agent(raw_text: str) -> ComplaintState:
    """Convenience wrapper the API calls with the complaint text."""
    return complaint_agent.invoke({"raw_text": raw_text})
