from typing import Dict, Any
from app.core.state import ResearchState
from app.core.logger import log_event
from app.modules.writer.service import generate_report_draft

def writer_node(state: ResearchState) -> Dict[str, Any]:
    """
    Writer Node function for LangGraph.
    Reads 'search_results' and 'research_question', generates/updates 'draft'.
    """
    question = state["research_question"]
    results = state.get("search_results", [])
    prev_draft = state.get("draft", "")
    missing = state.get("missing_topics", [])
    groq_key = state.get("groq_api_key")
    model_name = state.get("model_name")
    
    draft = generate_report_draft(
        research_question=question,
        search_results=results,
        previous_draft=prev_draft,
        missing_topics=missing,
        groq_api_key=groq_key,
        model_name=model_name
    )
    
    msg = f"Synthesized research draft ({len(draft.split())} words)."
    updated_logs = log_event(state.get("logs", []), "writer", msg)
    
    return {
        "draft": draft,
        "logs": updated_logs
    }
