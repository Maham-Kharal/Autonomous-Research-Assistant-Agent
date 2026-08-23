import streamlit as st
import sys
import os

# Ensure workspace root is on Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ui.components import inject_pastel_css, render_header
from ui.views import render_sidebar, render_node_event
from app.workflow.runner import run_research_stream

st.set_page_config(
    page_title="LangGraph Research Assistant Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom soft pastel CSS
inject_pastel_css()

# Render Header & Sidebar
render_header()
groq_key, tavily_key, selected_model = render_sidebar()

# Main Research Form
st.markdown("### 💬 Submit Your Research Question")
user_question = st.text_input(
    "Enter a topic or question to research:",
    value="",
    placeholder="e.g. Breakthroughs in solid-state batteries | Impact of Quantum Computing on Cybersecurity | Room-temperature superconductors | Fusion energy status"
)

start_button = st.button("🚀 Start Autonomous Research", type="primary", use_container_width=True)

if start_button:
    if not groq_key:
        st.error("Please enter a Groq API Key in the sidebar or set GROQ_API_KEY in your .env file!")
    elif not user_question.strip():
        st.warning("Please type a valid research question.")
    else:
        st.markdown("---")
        st.markdown("### 🔄 Graph Execution Trace")
        
        status_container = st.container()
        final_state = {}
        
        with status_container:
            progress_bar = st.progress(0, text=f"Initializing LangGraph execution ({selected_model})...")
            step_count = 0
            
            try:
                for event in run_research_stream(user_question.strip(), groq_key, tavily_key, selected_model):
                    step_count += 1
                    progress_pct = min(int((step_count / 7) * 100), 95)
                    progress_bar.progress(progress_pct, text=f"Step #{step_count} executing graph node...")
                    
                    for node_name, state_update in event.items():
                        render_node_event(node_name, state_update)
                        final_state.update(state_update)
                        
                progress_bar.progress(100, text="✅ Research workflow finished cleanly!")
                st.balloons()
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")

        if final_state and final_state.get("final_report"):
            st.markdown("---")
            st.markdown("### 📊 Final Research Publication")
            
            tab_report, tab_logs, tab_state = st.tabs(["📄 Final Report", "📜 Execution Logs", "🔍 Raw State Memory"])
            
            with tab_report:
                st.markdown('<div class="report-container">', unsafe_allow_html=True)
                st.markdown(final_state["final_report"])
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.download_button(
                    label="📥 Download Research Report (.md)",
                    data=final_state["final_report"],
                    file_name="research_report.md",
                    mime="text/markdown"
                )
                
            with tab_logs:
                st.markdown("#### Audit Step Trail")
                for log_entry in final_state.get("logs", []):
                    st.code(log_entry)
                    
            with tab_state:
                st.markdown("#### Shared State Memory Inspection")
                st.json({
                    "sub_questions": final_state.get("sub_questions", []),
                    "search_results_count": len(final_state.get("search_results", [])),
                    "revision_count": final_state.get("revision_count", 0),
                    "is_complete": final_state.get("is_complete", False),
                    "missing_topics": final_state.get("missing_topics", [])
                })
