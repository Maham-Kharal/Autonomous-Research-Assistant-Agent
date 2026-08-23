from langgraph.graph import StateGraph, START, END
from app.core.state import ResearchState
from app.modules.planner.node import planner_node
from app.modules.searcher.node import search_node
from app.modules.writer.node import writer_node
from app.modules.reviewer.node import reviewer_node
from app.modules.reviewer.router import check_review_status
from app.modules.finalizer.node import finalizer_node

def create_research_graph():
    """
    Constructs and compiles the Research Assistant LangGraph workflow.
    """
    builder = StateGraph(ResearchState)

    # 1. Register Nodes
    builder.add_node("planner", planner_node)
    builder.add_node("searcher", search_node)
    builder.add_node("writer", writer_node)
    builder.add_node("reviewer", reviewer_node)
    builder.add_node("finalizer", finalizer_node)

    # 2. Add Fixed Connections
    builder.add_edge(START, "planner")
    builder.add_edge("planner", "searcher")
    builder.add_edge("searcher", "writer")
    builder.add_edge("writer", "reviewer")

    # 3. Add Conditional Edge for Looping (reviewer -> searcher OR finalizer)
    builder.add_conditional_edges(
        "reviewer",
        check_review_status,
        {
            "searcher": "searcher",   # Loop back to search missing facts
            "finalizer": "finalizer"  # Proceed to finalize report
        }
    )

    # 4. Terminate at Finalizer
    builder.add_edge("finalizer", END)

    # 5. Compile state graph
    return builder.compile()

# Pre-compiled global graph instance
research_graph = create_research_graph()
