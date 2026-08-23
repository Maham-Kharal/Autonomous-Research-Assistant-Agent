from pydantic import BaseModel, Field

class FinalReportOutput(BaseModel):
    """Pydantic schema for final report formatting."""
    executive_summary: str = Field(description="Short 3-4 sentence high-level executive summary.")
    formatted_report: str = Field(description="Polished markdown report containing summary, detailed sections, and sources.")
