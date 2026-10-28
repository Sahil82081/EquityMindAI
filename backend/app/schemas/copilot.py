from typing import Optional
from pydantic import BaseModel, Field


class CopilotRequest(BaseModel):
    """User inquiry sent to the Research Copilot."""

    question: str = Field(..., description="User question regarding the research report")
    research_id: Optional[str] = Field(
        default=None,
        description="Research session ID identifying the target company's research state",
    )
    ticker: Optional[str] = Field(default=None, description="Optional stock ticker context")
    context: Optional[str] = Field(default=None, description="Optional extra evidence context")


class CopilotResponse(BaseModel):
    """Evidence-grounded response from the Research Copilot."""

    research_id: Optional[str] = Field(default=None, description="Associated research ID")
    question: str = Field(..., description="The original question answered")
    answer: str = Field(..., description="Evidence-backed answer anchored strictly to research findings")
    ticker: Optional[str] = Field(default=None, description="Associated ticker symbol")
    sources_cited: list[str] = Field(
        default_factory=list,
        description="Specific research components cited (e.g. 'SEC Filings', 'Claim 3', 'Bear Agent')",
    )
    is_grounded: bool = Field(
        default=True,
        description="True if answered directly from retrieved research evidence rather than general knowledge",
    )
    sample: bool = Field(default=False, description="False indicates authentic research grounding")
