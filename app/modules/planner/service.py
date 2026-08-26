from typing import List, Optional
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import get_llm, GROQ_MODEL_CANDIDATES
from app.modules.planner.schemas import PlannerOutput

PLANNER_SYSTEM_PROMPT = """You are an expert AI Research Architect.
Your task is to take a main research question and break it down into 3 to 5 distinct, highly targeted web search sub-queries.

Requirements:
- Output between 3 and 5 queries.
- Each query must address a specific aspect of the main question (background, technical details, current state, key challenges, or applications).
- Make queries search-engine friendly.
"""

def generate_research_plan(research_question: str, groq_api_key: Optional[str] = None, model_name: Optional[str] = None) -> List[str]:
    """Generates 3-5 sub-queries for a research question using Groq LLM with multi-model fallback."""
    models_to_try = [model_name] + [m for m in GROQ_MODEL_CANDIDATES if m != model_name] if model_name else GROQ_MODEL_CANDIDATES

    for m_name in models_to_try:
        if not m_name:
            continue
        try:
            llm = get_llm(groq_api_key, m_name)
            try:
                structured_llm = llm.with_structured_output(PlannerOutput)
                prompt = ChatPromptTemplate.from_messages([
                    ("system", PLANNER_SYSTEM_PROMPT),
                    ("user", "Research Question: {question}")
                ])
                chain = prompt | structured_llm
                result: PlannerOutput = chain.invoke({"question": research_question})
                if result and result.sub_questions and len(result.sub_questions) >= 3:
                    return result.sub_questions[:5]
            except Exception:
                pass

            # Text parsing fallback
            prompt = ChatPromptTemplate.from_messages([
                ("system", PLANNER_SYSTEM_PROMPT + "\nReturn sub-queries separated by newlines."),
                ("user", "Research Question: {question}")
            ])
            chain = prompt | llm
            raw_response = chain.invoke({"question": research_question})
            lines = [line.strip("- *12345.").strip() for line in raw_response.content.split("\n") if line.strip()]
            valid_queries = [q for q in lines if len(q) > 5]
            
            if len(valid_queries) >= 3:
                return valid_queries[:5]
        except Exception:
            # Catch 429 rate limits, 404s, 400s and switch to next model
            continue

    return [
        f"{research_question} overview and background",
        f"{research_question} key technical details and mechanisms",
        f"{research_question} recent developments and future outlook"
    ]
