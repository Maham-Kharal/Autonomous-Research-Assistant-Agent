from app.core.state import ResearchState

def check_review_status(state: ResearchState) -> str:
    """
    Conditional Edge Router for LangGraph.
    Evaluates state to route workflow:
    - If is_complete is True OR revision_count >= 3 -> route to 'finalizer' node.
    - Otherwise (missing topics & revision_count < 3) -> route back to 'searcher' node for looping.
    """
    is_complete = state.get("is_complete", False)
    revision_count = state.get("revision_count", 0)
    
    if is_complete or revision_count >= 3:
        return "finalizer"
    else:
        return "searcher"
