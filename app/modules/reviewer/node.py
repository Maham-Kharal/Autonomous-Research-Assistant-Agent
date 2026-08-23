from typing import Dict, Any
from app.core.state import ResearchState
from app.core.logger import log_event
from app.modules.reviewer.service import review_draft_quality

def reviewer_node(state: ResearchState) -> Dict[str, Any]:
    """
    Reviewer Node function for LangGraph.
    Reads draft, increments revision_count, checks for missing topics.
    """
    question = state["research_question"]
    draft = state.get("draft", "")
    current_count = state.get("revision_count", 0) + 1
    groq_key = state.get("groq_api_key")
    model_name = state.get("model_name")
    
    review_res = review_draft_quality(
        research_question=question,
        draft=draft,
        revision_count=current_count,
        groq_api_key=groq_key,
        model_name=model_name
    )
    
    status_str = "COMPLETE" if review_res.is_complete else f"INCOMPLETE (Gaps: {', '.join(review_res.missing_topics)})"
    msg = f"Review Round #{current_count}: Outcome -> {status_str}. Reason: {review_res.feedback_reason}"
    updated_logs = log_event(state.get("logs", []), "reviewer", msg)
    
    return {
        "revision_count": current_count,
        "is_complete": review_res.is_complete,
        "missing_topics": review_res.missing_topics,
        "logs": updated_logs
    }
