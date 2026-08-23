from typing import List, Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import get_llm, GROQ_MODEL_CANDIDATES

FINALIZER_SYSTEM_PROMPT = """You are an Executive Editor compiling the final publication report.
Your job is to polish the research draft and construct a clean, comprehensive final report.

Format Structure Required:
1. `# Executive Summary`: A concise 3-4 sentence high-level overview answering the main question directly.
2. `---`
3. `# Research Findings & Analysis`: The full, detailed research report structured with clear headers, key points, and inline citations.
4. `---`
5. `# References & Sources`: A clean bulleted list of all cited sources with Markdown links. Format: `- [Title](URL) - Source Type`.
"""

def generate_final_report(
    research_question: str,
    draft: str,
    search_results: List[Dict[str, Any]],
    groq_api_key: Optional[str] = None,
    model_name: Optional[str] = None
) -> str:
    """Formats the final polished report with Executive Summary and References."""
    sources_text = ""
    seen_urls = set()
    for item in search_results:
        title = item.get("title", "Web Link")
        url = item.get("url", "#")
        stype = item.get("source_type", "Web Search")
        if url != "#" and url not in seen_urls:
            seen_urls.add(url)
            sources_text += f"- [{title}]({url}) ({stype})\n"
            
    if not sources_text:
        sources_text = "- Web search data aggregated during research steps."

    models_to_try = [model_name] + [m for m in GROQ_MODEL_CANDIDATES if m != model_name] if model_name else GROQ_MODEL_CANDIDATES

    for m_name in models_to_try:
        if not m_name:
            continue
        try:
            llm = get_llm(groq_api_key, m_name)
            prompt = ChatPromptTemplate.from_messages([
                ("system", FINALIZER_SYSTEM_PROMPT),
                ("user", "Research Question: {question}\n\nDraft Section:\n{draft}\n\nSources Collected:\n{sources}")
            ])
            chain = prompt | llm
            response = chain.invoke({
                "question": research_question,
                "draft": draft,
                "sources": sources_text
            })
            final_output = response.content
            if "# References & Sources" not in final_output:
                final_output += f"\n\n---\n# References & Sources\n{sources_text}"
            return final_output
        except Exception as e:
            err = str(e).lower()
            if any(k in err for k in ["model_decommissioned", "model_not_found", "400", "404", "decommissioned", "not exist", "no longer supported"]):
                continue
            raise e

    return f"# Executive Summary\n\n{draft}\n\n---\n# References & Sources\n{sources_text}"
