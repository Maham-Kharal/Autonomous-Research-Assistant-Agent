from pydantic import BaseModel, Field
from typing import List

class ReviewOutput(BaseModel):
    """Pydantic schema for quality review assessment."""
    is_complete: bool = Field(
        description="True if the draft adequately and thoroughly answers the main question without major information gaps. False if important details or aspects are missing."
    )
    missing_topics: List[str] = Field(
        default_factory=list,
        description="If is_complete is False, list 1 to 3 specific sub-topics or queries that need further web research."
    )
    feedback_reason: str = Field(
        description="Short 1-2 sentence explanation of the review assessment."
    )
