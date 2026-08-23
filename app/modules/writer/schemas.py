from pydantic import BaseModel, Field

class DraftOutput(BaseModel):
    """Pydantic schema for draft report output."""
    draft_content: str = Field(description="Comprehensive markdown draft section synthesized from web search results.")
