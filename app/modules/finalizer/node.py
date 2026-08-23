from typing import Dict, Any
from app.core.state import ResearchState
from app.core.logger import log_event
from app.modules.finalizer.service import generate_final_report

def finalizer_node(state: ResearchState) -> Dict[str, Any]:
    """
    Finalizer Node function for LangGraph.
    Reads draft and search_results, produces 'final_report'.
    """
    question = state["research_question"]
    draft = state.get("draft", "")
    results = state.get("search_results", [])
    groq_key = state.get("groq_api_key")
    model_name = state.get("model_name")
    
    final_report = generate_final_report(
        research_question=question,
        draft=draft,
        search_results=results,
        groq_api_key=groq_key,
        model_name=model_name
    )
    
    msg = "Finalized executive summary, full report sections, and cited sources list."
    updated_logs = log_event(state.get("logs", []), "finalizer", msg)
    
    return {
        "final_report": final_report,
        "logs": updated_logs
    }
