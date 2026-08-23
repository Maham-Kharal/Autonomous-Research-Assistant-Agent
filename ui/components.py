import streamlit as st

PASTEL_CSS = """
<style>
/* Main Background & Font Styling */
.main {
    background-color: #F9FBFD;
    color: #2C3E50;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Custom Header Badge */
.header-container {
    background: linear-gradient(135deg, #E8F0FE 0%, #F0E6FF 100%);
    padding: 2rem;
    border-radius: 16px;
    border: 1px solid #E1E8ED;
    margin-bottom: 2rem;
    box-shadow: 0 4px 12px rgba(123, 140, 222, 0.08);
}

.header-title {
    color: #3A4B8C;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.header-subtitle {
    color: #6C7A89;
    font-size: 1.05rem;
    font-weight: 400;
}

/* Pastel Cards for Graph Nodes */
.node-card {
    background-color: #FFFFFF;
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    border-left: 5px solid #7B8CDE;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.node-card-planner { border-left-color: #7B8CDE; background-color: #F8F9FE; }
.node-card-searcher { border-left-color: #82B1FF; background-color: #F5F9FF; }
.node-card-writer { border-left-color: #B388FF; background-color: #FAF5FF; }
.node-card-reviewer { border-left-color: #80CBC4; background-color: #F4FBFB; }
.node-card-finalizer { border-left-color: #A5D6A7; background-color: #F5FAF5; }

/* Status Badges */
.badge-mint {
    background-color: #E6F4EA;
    color: #137333;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.85rem;
    display: inline-block;
}

.badge-lavender {
    background-color: #F3E8FF;
    color: #6B21A8;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.85rem;
    display: inline-block;
}

.badge-softblue {
    background-color: #E8F0FE;
    color: #1A73E8;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.85rem;
    display: inline-block;
}

/* Custom Output Report Card */
.report-container {
    background-color: #FFFFFF;
    border-radius: 16px;
    padding: 2rem;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.03);
}
</style>
"""

def inject_pastel_css():
    """Injects custom soft pastel CSS styling into Streamlit app."""
    st.markdown(PASTEL_CSS, unsafe_allow_html=True)

def render_header():
    """Renders the main header banner with soft pastel styling."""
    st.markdown("""
        <div class="header-container">
            <div class="header-title">🧠 Autonomous Research Assistant Agent</div>
            <div class="header-subtitle">Powered by <b>LangGraph</b>, <b>Groq LLM</b>, and <b>Tavily Web Search</b> — Featuring Self-Review & Infinite-Loop Prevention</div>
        </div>
    """, unsafe_allow_html=True)
