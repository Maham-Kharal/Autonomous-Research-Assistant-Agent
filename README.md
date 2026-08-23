# Autonomous Research Assistant Agent (LangGraph Portfolio Project)

An autonomous, looping AI Research Assistant Agent built with **LangGraph**, **Groq LLM** (`llama-3.3-70b-versatile`), **Tavily AI Search**, and **Streamlit** styled in soft pastel colors.

---

## 🌟 Key Features & Requirements Met

- **Sub-Task Decomposition**: Breaks complex research questions into 3-5 sub-queries (`planner_node`).
- **Resilient Web Search**: Executes AI search via **Tavily** with automatic, zero-config fallback to **DuckDuckGo** (`search_node`).
- **State Memory**: Stores all search items, section drafts, and audit step logs in a shared graph state dictionary (`ResearchState`).
- **Self-Critique & Gap Filling**: Evaluates draft quality and identifies missing topics (`reviewer_node`).
- **Controlled Graph Looping**: Loops back to search for missing topics, enforcing a strict **max 3 revision rounds** safety cap (`router.py`).
- **Final Report & Source Citation**: Formats executive summaries, detailed analysis sections, and Markdown source citations (`finalizer_node`).
- **Live Streamed UI**: Real-time visual step streaming built with a soft pastel Streamlit theme (`app.py`).

---

## 🏗 Project Architecture & Structure

The codebase uses a **Feature-Driven Modular Architecture**:

```
lang-graph/
├── .streamlit/
│   └── config.toml             # Custom soft pastel theme
├── app/
│   ├── core/
│   │   ├── config.py           # Groq & Tavily API settings
│   │   ├── state.py            # Shared ResearchState memory definition
│   │   └── logger.py           # Timestamped audit logger
│   ├── modules/
│   │   ├── planner/            # Sub-query decomposition (node.py, service.py, schemas.py)
│   │   ├── searcher/           # Web search execution (node.py, service.py, schemas.py)
│   │   ├── writer/             # Report drafting (node.py, service.py, schemas.py)
│   │   ├── reviewer/           # Quality critique & router (node.py, service.py, router.py, schemas.py)
│   │   └── finalizer/          # Final report & sources layout (node.py, service.py, schemas.py)
│   └── workflow/
│       ├── graph.py            # LangGraph StateGraph builder & compilation
│       └── runner.py           # Step streaming execution runner
├── ui/
│   ├── components.py           # Pastel CSS injection & styled header
│   └── views.py                # Sidebar controls & graph node step renderers
├── app.py                      # Main Streamlit application launcher
├── requirements.txt            # Python dependencies
└── .env.example                # Secrets template
```

---

## 🚀 Quickstart (Local Setup)

1. **Clone & Navigate**:
   ```bash
   cd lang-graph
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   Add your `GROQ_API_KEY` (Get a free key at [console.groq.com](https://console.groq.com/)). Option: add `TAVILY_API_KEY` (from [tavily.com](https://tavily.com/)).

4. **Launch Streamlit App**:
   ```bash
   python -m streamlit run streamlit_app.py
   ```

---

## ☁️ Step-by-Step Deployment Guide (Streamlit Community Cloud)

You can deploy this application publicly for **free** on Streamlit Community Cloud in 4 easy steps:

### Step 1: Push Code to GitHub
Ensure all code is committed and pushed to a public GitHub repository:
```bash
git init
git add .
git commit -m "Deploy LangGraph Research Assistant Agent"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

### Step 2: Sign in to Streamlit Community Cloud
Visit [share.streamlit.io](https://share.streamlit.io/) and log in using your GitHub account.

### Step 3: Create a New App
1. Click the **"Create app"** button.
2. Select your GitHub repository (`YOUR_USERNAME/YOUR_REPOSITORY`).
3. Set **Branch** to `main`.
4. Set **Main file path** to `app.py`.

### Step 4: Add Environment Secrets & Deploy
1. Click **"Advanced settings..."** (or **"Secrets"**).
2. Enter your API keys in TOML format:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   TAVILY_API_KEY = "your_tavily_api_key_here"
   ```
3. Click **"Deploy!"**.
4. Streamlit will build your app and generate a public, shareable URL!
