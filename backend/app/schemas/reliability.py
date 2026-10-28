from pydantic import BaseModel, Field


class ReliabilityMetrics(BaseModel):
    """Component scores for the four measurable factors of Research Reliability."""

    evidence_quality: int = Field(
        ...,
        ge=0,
        le=100,
        description="Measures data source provenance (SEC filings, verified market data, authenticated news feeds)",
    )
    claim_verification: int = Field(
        ...,
        ge=0,
        le=100,
        description="Measures the proportion of empirical research claims that were recomputed and matched in Python",
    )
    source_coverage: int = Field(
        ...,
        ge=0,
        le=100,
        description="Measures availability and completeness of required research inputs (prices, filings, news, baselines)",
    )
    agent_agreement: int = Field(
        ...,
        ge=0,
        le=100,
        description="Measures logical alignment and consistency across independent research agents in the pipeline",
    )


class MetricBreakdown(BaseModel):
    """Dimensional breakdown item for the Research Reliability UI."""

    name: str = Field(..., description="Reliability dimension name e.g. 'Evidence Quality'")
    score: int = Field(..., ge=0, le=100, description="Percentage score (0-100)")
    description: str = Field(..., description="Explanation of what this dimension measures")


class ReliabilityScore(BaseModel):
    """Research Reliability Score.

    CRITICAL TERMINOLOGY:
    This measures how reliable the research process and evidence are.
    It is NOT an investment probability, stock prediction probability, guaranteed confidence, or return probability.
    """

    score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Deterministic weighted Research Reliability Score (0-100)",
    )
    overall_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Backward-compatible alias for score",
    )
    metrics: ReliabilityMetrics = Field(
        ...,
        description="Key measurable component metrics",
    )
    breakdown: list[MetricBreakdown] = Field(
        default_factory=list,
        description="Ordered list of metric breakdown cards for UI display",
    )
