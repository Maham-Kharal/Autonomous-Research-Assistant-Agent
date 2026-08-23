from pydantic import BaseModel, Field
from typing import List

class PlannerOutput(BaseModel):
    """Pydantic schema for structured planning output."""
    sub_questions: List[str] = Field(
        description="List of 3 to 5 targeted, distinct research sub-queries to search on the web."
    )
