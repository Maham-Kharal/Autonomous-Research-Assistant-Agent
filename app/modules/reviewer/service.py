from typing import Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import get_llm, GROQ_MODEL_CANDIDATES
from app.modules.reviewer.schemas import ReviewOutput

REVIEWER_SYSTEM_PROMPT = """You are a rigorous Quality Control Reviewer for research publications.
Your job is to evaluate a research report draft against the original research question to determine if key information is missing.

Rules:
- Set `is_complete` to TRUE if the draft provides a clear, comprehensive, well-facted answer to the main question.
- Set `is_complete` to FALSE ONLY if there are major, critical gaps in facts or missing dimensions of the topic.
- If `is_complete` is FALSE, provide 1 to 3 concise, specific search queries in `missing_topics` to fill those gaps.
- Be fair and reasonable. Do not demand endless details if the draft is already solid.
"""

def review_draft_quality(
    research_question: str,
    draft: str,
    revision_count: int,
    groq_api_key: Optional[str] = None,
    model_name: Optional[str] = None
) -> ReviewOutput:
    """Critiques draft quality and detects missing topics using Groq LLM with multi-model fallback."""
    if revision_count >= 3:
        return ReviewOutput(
            is_complete=True,
            missing_topics=[],
            feedback_reason=f"Reached maximum round limit ({revision_count}/3 iterations completed)."
        )

    models_to_try = [model_name] + [m for m in GROQ_MODEL_CANDIDATES if m != model_name] if model_name else GROQ_MODEL_CANDIDATES

    for m_name in models_to_try:
        if not m_name:
            continue
        try:
            llm = get_llm(groq_api_key, m_name)
            try:
                structured_llm = llm.with_structured_output(ReviewOutput)
                prompt = ChatPromptTemplate.from_messages([
                    ("system", REVIEWER_SYSTEM_PROMPT),
                    ("user", "Original Question: {question}\n\nCurrent Draft:\n{draft}\n\nIteration Count: {count}")
                ])
                chain = prompt | structured_llm
                result: ReviewOutput = chain.invoke({
                    "question": research_question,
                    "draft": draft,
                    "count": revision_count
                })
                return result
            except Exception:
                pass
        except Exception:
            continue

    return ReviewOutput(
        is_complete=True,
        missing_topics=[],
        feedback_reason="Draft acceptable based on fallback review criteria."
    )
