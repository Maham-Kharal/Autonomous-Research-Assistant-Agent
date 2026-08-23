from typing import Dict, Any
from app.core.state import ResearchState
from app.core.logger import log_event
from app.modules.planner.service import generate_research_plan

def planner_node(state: ResearchState) -> Dict[str, Any]:
    """
    Planner Node function for LangGraph.
    Reads 'research_question' from state and populates 'sub_questions'.
    """
    question = state["research_question"]
    groq_key = state.get("groq_api_key")
    model_name = state.get("model_name")
    
    sub_qs = generate_research_plan(question, groq_key, model_name)
    
    msg = f"Decomposed question into {len(sub_qs)} search steps: {', '.join(sub_qs)}"
    updated_logs = log_event(state.get("logs", []), "planner", msg)
    
    return {
        "sub_questions": sub_qs,
        "logs": updated_logs
    }
