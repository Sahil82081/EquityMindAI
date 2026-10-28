from typing import Optional
from pydantic import BaseModel, Field


class NewsSynthesisOutput(BaseModel):
    """Pydantic validated structured output from Gemini for news summarization."""

    executive_summary: str = Field(
        ..., description="Synthesized executive summary of authentic company news"
    )
    key_themes: list[str] = Field(
        default_factory=list, description="Core themes identified across news articles"
    )
    sentiment_reasoning: str = Field(
        ..., description="Explanation of why market coverage is positive, negative, or neutral"
    )
    catalysts: list[str] = Field(
        default_factory=list, description="Notable operational, strategic, or regulatory catalysts"
    )


class ValuationReasoningOutput(BaseModel):
    """Pydantic validated structured output from Gemini for valuation reasoning."""

    multiple_assessment: str = Field(
        ..., description="Analytical reasoning on the P/E multiple vs industry/market norms"
    )
    growth_vs_multiple: str = Field(
        ..., description="Evaluation of whether YoY revenue growth justifies the current multiple"
    )
    margin_durability: str = Field(
        ..., description="Assessment of operating and net profit margin sustainability"
    )
    historical_discount_or_premium: str = Field(
        ..., description="Interpretation of the multiple variance vs 5-year historical average"
    )
    executive_summary: str = Field(
        ..., description="Comprehensive executive valuation narrative grounded in the verified metrics"
    )
