import os
from typing import Optional, List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from groq import Groq

load_dotenv()

# Active Groq model IDs with required provider prefixes
GROQ_MODEL_CANDIDATES = [
    "openai/gpt-oss-120b",
    "qwen/qwen3.6-27b",
    "openai/gpt-oss-20b",
    "groq/compound",
    "groq/compound-mini"
]

DEFAULT_GROQ_MODEL = "openai/gpt-oss-120b"

def get_groq_api_key(override_key: Optional[str] = None) -> Optional[str]:
    """Retrieve Groq API key safely without exposing secrets in UI."""
    key = override_key
    if not key or not key.strip():
        key = os.getenv("GROQ_API_KEY")
    if not key or not key.strip():
        try:
            import streamlit as st
            if "GROQ_API_KEY" in st.secrets:
                key = st.secrets["GROQ_API_KEY"]
        except Exception:
            pass
    if key and key.strip():
        return key.strip()
    return None

def get_tavily_api_key(override_key: Optional[str] = None) -> Optional[str]:
    """Retrieve Tavily API key safely without exposing secrets in UI."""
    key = override_key
    if not key or not key.strip():
        key = os.getenv("TAVILY_API_KEY")
    if not key or not key.strip():
        try:
            import streamlit as st
            if "TAVILY_API_KEY" in st.secrets:
                key = st.secrets["TAVILY_API_KEY"]
        except Exception:
            pass
    if key and key.strip():
        return key.strip()
    return None

def get_active_groq_models(api_key: str) -> List[str]:
    """Queries Groq API dynamically for live text generation models."""
    try:
        client = Groq(api_key=api_key)
        models_data = client.models.list().data
        valid_models = []
        for m in models_data:
            m_id = m.id
            if not any(ex in m_id.lower() for ex in ["whisper", "guard", "audio", "orpheus"]):
                valid_models.append(m_id)
        if valid_models:
            return valid_models
    except Exception:
        pass
    return GROQ_MODEL_CANDIDATES

def get_llm(groq_api_key: Optional[str] = None, model_name: Optional[str] = None) -> ChatGroq:
    """Instantiates ChatGroq model instance."""
    api_key = get_groq_api_key(groq_api_key)
    if not api_key:
        raise ValueError("Groq API Key is missing. Please provide a valid GROQ_API_KEY.")
    
    target_model = model_name or DEFAULT_GROQ_MODEL
    return ChatGroq(
        groq_api_key=api_key,
        model_name=target_model,
        temperature=0.2,
        max_retries=2
    )

def invoke_llm_with_fallback(chain_or_prompt, input_dict: dict, groq_api_key: Optional[str] = None, model_name: Optional[str] = None):
    """
    Executes an LLM chain with multi-model fallback across active Groq models.
    Catches 404 model_not_found, 400 decommissioned, AND 429 rate_limit_exceeded errors automatically.
    """
    api_key = get_groq_api_key(groq_api_key)
    if not api_key:
        raise ValueError("Groq API Key is missing.")
        
    active_models = get_active_groq_models(api_key)
    requested_model = model_name or active_models[0]
    
    models_to_try = [requested_model] + [m for m in active_models if m != requested_model]
    
    last_exception = None
    for m_name in models_to_try:
        if not m_name:
            continue
        try:
            llm = ChatGroq(groq_api_key=api_key, model_name=m_name, temperature=0.2)
            if hasattr(chain_or_prompt, "first"):
                prompt_template = chain_or_prompt.first
                chain = prompt_template | llm
                return chain.invoke(input_dict)
            else:
                return llm.invoke(input_dict)
        except Exception as e:
            # Catch all model failures (rate limit 429, decommissioned 400, not found 404) and switch to next model candidate
            last_exception = e
            continue
                
    raise last_exception if last_exception else RuntimeError("No active Groq model candidates succeeded.")
