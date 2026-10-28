from typing import Optional, Literal
from pydantic import BaseModel, Field
from .gemini_outputs import NewsSynthesisOutput


class NewsArticle(BaseModel):
    """Structured representation of an authentic news article."""

    headline: str = Field(..., description="Authentic article headline")
    source: str = Field(..., description="Legitimate publisher or publication source e.g. CNBC, Reuters, Bloomberg")
    published_at: str = Field(..., description="Publication date/time formatted string or ISO timestamp")
    url: str = Field(..., description="Legitimate, authentic article URL")
    summary: str = Field(..., description="Article summary or description snippet from feed")
    sentiment: Literal["positive", "negative", "neutral"] = Field(
        ..., description="Sentiment classification category"
    )
    sentiment_score: Optional[float] = Field(
        default=None, description="Polarity score ranging from -1.0 (very negative) to +1.0 (very positive)"
    )


class NewsResearchResult(BaseModel):
    """Aggregate output from NewsAgent."""

    ticker: str = Field(..., description="Target ticker symbol")
    company_name: str = Field(..., description="Resolved company name")
    articles: list[NewsArticle] = Field(default_factory=list, description="List of authentic news articles")
    overall_sentiment: str = Field(default="neutral", description="Aggregated market news sentiment")
    positive_count: int = Field(default=0, description="Count of positive articles")
    negative_count: int = Field(default=0, description="Count of negative articles")
    neutral_count: int = Field(default=0, description="Count of neutral articles")
    total_articles: int = Field(default=0, description="Total count of articles retrieved")
    source_coverage: str = Field(default="Legitimate financial RSS and wire sources", description="News source description")
    synthesis: Optional[NewsSynthesisOutput] = Field(
        default=None, description="Gemini news reasoning and summarization validated with Pydantic"
    )
