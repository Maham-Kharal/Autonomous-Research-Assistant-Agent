from typing import List, Dict, Any, Optional
import warnings

# Suppress duckduckgo_search renaming warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="duckduckgo_search")
warnings.filterwarnings("ignore", category=ResourceWarning)

try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS

from tavily import TavilyClient
from app.core.config import get_tavily_api_key

def execute_single_search(query: str, tavily_api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Executes a web search safely for a single query string.
    Uses Tavily as primary AI search tool if API key available,
    otherwise falls back smoothly to DDGS (DuckDuckGo) search.
    """
    api_key = get_tavily_api_key(tavily_api_key)
    results = []
    
    # Try Tavily Search first if API key exists
    if api_key:
        try:
            client = TavilyClient(api_key=api_key)
            tavily_res = client.search(query=query, max_results=3, search_depth="basic")
            for item in tavily_res.get("results", []):
                results.append({
                    "query": query,
                    "title": item.get("title", "Untitled Web Result"),
                    "url": item.get("url", "#"),
                    "snippet": item.get("content", item.get("snippet", "")),
                    "source_type": "Tavily AI Search"
                })
            if results:
                return results
        except Exception:
            pass

    # Fallback to DDGS Search
    try:
        ddgs = DDGS()
        ddg_res = list(ddgs.text(query, max_results=3))
        for item in ddg_res:
            results.append({
                "query": query,
                "title": item.get("title", "Untitled Result"),
                "url": item.get("href", "#"),
                "snippet": item.get("body", ""),
                "source_type": "DuckDuckGo Search"
            })
    except Exception as e:
        results.append({
            "query": query,
            "title": f"Search notice for '{query}'",
            "url": "#",
            "snippet": f"Web search could not retrieve live data for '{query}' (Network/Rate limit restriction). Proceeding with general knowledge.",
            "source_type": "Search Error Handling"
        })
        
    return results

def execute_batch_search(queries: List[str], tavily_api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """Executes searches for a list of queries and aggregates unique results."""
    all_results = []
    seen_urls = set()
    
    for q in queries:
        items = execute_single_search(q, tavily_api_key)
        for item in items:
            url = item.get("url")
            if url and url != "#" and url in seen_urls:
                continue
            if url and url != "#":
                seen_urls.add(url)
            all_results.append(item)
            
    return all_results
