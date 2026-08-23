from typing import Generator, Dict, Any, Optional
from app.workflow.graph import research_graph

def run_research_stream(
    research_question: str,
    groq_api_key: Optional[str] = None,
    tavily_api_key: Optional[str] = None,
    model_name: Optional[str] = None
) -> Generator[Dict[str, Any], None, None]:
    """
    Executes the research graph and yields streaming state updates as each node completes.
    """
    initial_state = {
        "research_question": research_question,
        "sub_questions": [],
        "search_results": [],
        "draft": "",
        "missing_topics": [],
        "revision_count": 0,
        "is_complete": False,
        "final_report": "",
        "logs": [],
        "groq_api_key": groq_api_key,
        "tavily_api_key": tavily_api_key,
        "model_name": model_name
    }

    for event in research_graph.stream(initial_state):
        yield event
