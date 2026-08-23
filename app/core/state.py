from typing import TypedDict, List, Dict, Any, Optional

class ResearchState(TypedDict):
    """
    Central memory state dictionary for the LangGraph Research Assistant Agent.
    Passed through every node in the state graph.
    """
    research_question: str                  # Original user question
    sub_questions: List[str]               # 3 to 5 broken-down research queries
    search_results: List[Dict[str, Any]]    # Collected web search articles & snippets
    draft: str                             # Synthesized draft report section
    missing_topics: List[str]              # Topics identified as missing by Reviewer
    revision_count: int                    # Loop counter (0 to 3 max)
    is_complete: bool                      # Flag set by Reviewer when satisfactory
    final_report: str                      # Final compiled report markdown
    logs: List[str]                        # Audit trace of step execution
    groq_api_key: Optional[str]            # Optional runtime API key pass-through
    tavily_api_key: Optional[str]          # Optional runtime API key pass-through
    model_name: Optional[str]              # Selected Groq model name
