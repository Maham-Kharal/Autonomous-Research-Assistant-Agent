from typing import List, Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import get_llm, GROQ_MODEL_CANDIDATES

WRITER_SYSTEM_PROMPT = """You are an expert Research Analyst & Technical Writer.
Your goal is to write a comprehensive, well-structured research draft addressing the main research question based ONLY on the provided web search findings.

Guidelines:
- Organize with clear markdown headers (`##`, `###`).
- Synthesize facts, technical mechanisms, key players, current trends, and challenges.
- Explicitly cite information sources inline using square brackets like `[Source: Title/URL]`.
- Do not make up facts not present in the search data.
"""

def generate_report_draft(
    research_question: str,
    search_results: List[Dict[str, Any]],
    previous_draft: str = "",
    missing_topics: List[str] = None,
    groq_api_key: Optional[str] = None,
    model_name: Optional[str] = None
) -> str:
    """Synthesizes search results into a detailed research report draft using Groq LLM with fallback."""
    formatted_context = ""
    for idx, item in enumerate(search_results, 1):
        title = item.get("title", "Source")
        url = item.get("url", "#")
        snippet = item.get("snippet", "")
        formatted_context += f"\n--- Source {idx} ---\nTitle: {title}\nURL: {url}\nSnippet: {snippet}\n"

    extra_instructions = ""
    if previous_draft and missing_topics:
        extra_instructions = f"\nNote: A previous draft exists. Please revise and expand it to address these missing topics: {', '.join(missing_topics)}."

    models_to_try = [model_name] + [m for m in GROQ_MODEL_CANDIDATES if m != model_name] if model_name else GROQ_MODEL_CANDIDATES

    for m_name in models_to_try:
        if not m_name:
            continue
        try:
            llm = get_llm(groq_api_key, m_name)
            prompt = ChatPromptTemplate.from_messages([
                ("system", WRITER_SYSTEM_PROMPT),
                ("user", "Main Research Question: {question}\n{extra}\n\nSearch Context Findings:\n{context}")
            ])
            chain = prompt | llm
            response = chain.invoke({
                "question": research_question,
                "extra": extra_instructions,
                "context": formatted_context if formatted_context else "No specific web results available."
            })
            return response.content
        except Exception as e:
            err = str(e).lower()
            if any(k in err for k in ["model_decommissioned", "model_not_found", "400", "404", "decommissioned", "not exist", "no longer supported"]):
                continue
            raise e

    raise RuntimeError("Failed to generate report draft across all Groq model candidates.")
