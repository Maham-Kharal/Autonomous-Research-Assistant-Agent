import streamlit as st
from typing import Dict, Any, Tuple
from app.core.config import get_groq_api_key, get_tavily_api_key, GROQ_MODEL_CANDIDATES

def render_sidebar() -> Tuple[str, str, str]:
    """Renders sidebar settings safely without populating secret keys into text input values."""
    with st.sidebar:
        st.markdown("### ⚙️ API Configuration")
        
        # User input fields default to empty string so pre-configured keys are NEVER visible in plain text
        groq_input = st.text_input(
            "Groq API Key (Optional Override)",
            value="",
            type="password",
            help="Leave blank to use system pre-configured Secrets."
        )
        
        model_options = GROQ_MODEL_CANDIDATES + ["Custom Model..."]
        selected_option = st.selectbox(
            "Groq LLM Model",
            options=model_options,
            index=0,
            help="Select your Groq LLM model. Fallback candidates kick in if model is unavailable."
        )
        
        if selected_option == "Custom Model...":
            selected_model = st.text_input("Enter Custom Groq Model Name", value="openai/gpt-oss-120b")
        else:
            selected_model = selected_option
        
        tavily_input = st.text_input(
            "Tavily API Key (Optional Override)",
            value="",
            type="password",
            help="Leave blank to use system Secrets or DuckDuckGo fallback."
        )
        
        # Resolve active keys safely without displaying them
        active_groq = get_groq_api_key(groq_input)
        active_tavily = get_tavily_api_key(tavily_input)
        
        st.markdown("---")
        st.markdown("### 📌 Active System Status")
        
        if active_groq:
            st.markdown(f'<span class="badge-mint">✓ Groq ({selected_model}) Active</span>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Groq API Key required to run.")
            
        if active_tavily:
            st.markdown('<span class="badge-lavender">✓ Tavily AI Search Enabled</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="badge-softblue">ℹ DuckDuckGo Free Search (Fallback)</span>', unsafe_allow_html=True)
            
        st.markdown("---")
        st.markdown("### 🔄 Graph Loop Policy")
        st.markdown("- **Max Revision Rounds**: 3 Loops")
        st.markdown("- **Safety Guard**: Prevents infinite loops & budget overruns.")
        
    return groq_input, tavily_input, selected_model

def render_node_event(node_name: str, state_update: Dict[str, Any]):
    """Renders a soft pastel card for each node execution during graph streaming."""
    if node_name == "planner":
        sub_qs = state_update.get("sub_questions", [])
        st.markdown(f"""
            <div class="node-card node-card-planner">
                <b>📋 Planner Node</b> — Generated {len(sub_qs)} search sub-queries:<br>
                <ul>{''.join([f'<li>{q}</li>' for q in sub_qs])}</ul>
            </div>
        """, unsafe_allow_html=True)
        
    elif node_name == "searcher":
        results = state_update.get("search_results", [])
        st.markdown(f"""
            <div class="node-card node-card-searcher">
                <b>🔍 Searcher Node</b> — Total web sources collected: <b>{len(results)} items</b>
            </div>
        """, unsafe_allow_html=True)
        
    elif node_name == "writer":
        draft = state_update.get("draft", "")
        word_count = len(draft.split())
        st.markdown(f"""
            <div class="node-card node-card-writer">
                <b>✍️ Writer Node</b> — Synthesized report draft (<b>{word_count} words</b>).
            </div>
        """, unsafe_allow_html=True)
        
    elif node_name == "reviewer":
        revision = state_update.get("revision_count", 0)
        is_complete = state_update.get("is_complete", False)
        missing = state_update.get("missing_topics", [])
        
        status_badge = '<span class="badge-mint">COMPLETE</span>' if is_complete else '<span class="badge-lavender">NEEDS GAPS FILLED</span>'
        missing_str = f"<br>Missing Topics: <i>{', '.join(missing)}</i>" if missing else ""
        
        st.markdown(f"""
            <div class="node-card node-card-reviewer">
                <b>🧐 Reviewer Node</b> (Iteration #{revision}/3) — Status: {status_badge} {missing_str}
            </div>
        """, unsafe_allow_html=True)
        
    elif node_name == "finalizer":
        st.markdown("""
            <div class="node-card node-card-finalizer">
                <b>📄 Finalizer Node</b> — Compiled Executive Summary & Formatted Sources list.
            </div>
        """, unsafe_allow_html=True)
