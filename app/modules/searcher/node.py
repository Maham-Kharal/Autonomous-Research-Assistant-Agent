from typing import Dict, Any
from app.core.state import ResearchState
from app.core.logger import log_event
from app.modules.searcher.service import execute_batch_search

def search_node(state: ResearchState) -> Dict[str, Any]:
    """
    Searcher Node function for LangGraph.
    Fetches web search results for sub-questions or missing topics.
    Appends new items to state['search_results'].
    """
    tavily_key = state.get("tavily_api_key")
    existing_results = list(state.get("search_results", []))
    missing_topics = state.get("missing_topics", [])
    
    # Decide which queries to run
    if missing_topics:
        queries_to_run = missing_topics[:3]
        query_type = "missing topics gap analysis"
    else:
        queries_to_run = state.get("sub_questions", [])
        query_type = "initial research plan sub-queries"
        
    new_results = execute_batch_search(queries_to_run, tavily_key)
    combined_results = existing_results + new_results
    
    msg = f"Executed search for {len(queries_to_run)} {query_type}. Collected {len(new_results)} web search items."
    updated_logs = log_event(state.get("logs", []), "searcher", msg)
    
    return {
        "search_results": combined_results,
        "logs": updated_logs
    }
