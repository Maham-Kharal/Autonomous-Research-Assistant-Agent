from pydantic import BaseModel, Field
from typing import Optional

class SearchResultItem(BaseModel):
    """Schema representing a single web search result item."""
    query: str = Field(description="The search query used")
    title: str = Field(description="Article or page title")
    url: str = Field(description="Source URL link")
    snippet: str = Field(description="Extracted summary snippet or body content")
    source_type: str = Field(default="web", description="tavily or duckduckgo")
