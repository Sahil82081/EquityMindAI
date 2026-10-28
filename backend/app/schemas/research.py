from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from .company import Company


class ResearchStatus(str, Enum):
    IDLE = "idle"
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ResearchRequest(BaseModel):
    company: Company = Field(..., description="Target company for research")


from .verification import (
    VerificationStatus,
    Evidence,
    VerificationResult,
    ClaimProof,
    Claim,
)


from .reliability import (
    ReliabilityMetrics,
    MetricBreakdown,
    ReliabilityScore,
)


from .financial import FinancialData, SnapshotMetric, RevenueYearItem
from .news import NewsResearchResult
from .valuation import ValuationAnalysis
from .debate import DebatePoint, DebateSide, DebateResult


class ResearchThesis(BaseModel):
    sentiment_badge: str = Field(..., description="Thesis summary e.g. Neutral, leaning bullish")
    sentiment_class: str = Field(..., description="CSS badge class e.g. b-warn, b-ok, b-bad")
    summary: str = Field(..., description="Narrative thesis executive summary")


class ResearchReport(BaseModel):
    thesis: ResearchThesis = Field(..., description="Core investment thesis")
    key_strengths: list[str] = Field(default_factory=list, description="Verified bull strengths")
    key_risks: list[str] = Field(default_factory=list, description="Core structural risks")
    financial_snapshot: list[SnapshotMetric] = Field(default_factory=list, description="Financial overview")
    conclusion: str = Field(..., description="Judge and analyst final recommendation summary")


class ResearchResponse(BaseModel):
    research_id: str = Field(..., description="Unique research tracking identifier")
    company: Company = Field(..., description="Company researched")
    status: ResearchStatus = Field(default=ResearchStatus.COMPLETED, description="Research state")
    created_at: str = Field(..., description="Timestamp of research creation")
    report: Optional[ResearchReport] = Field(default=None, description="Full research report")
    debate: Optional[DebateResult] = Field(default=None, description="Bull/Bear debate output")
    claims: list[Claim] = Field(default_factory=list, description="Audited claims chain")
    reliability_score: Optional[ReliabilityScore] = Field(default=None, description="Reliability score")
    financial_data: Optional[FinancialData] = Field(default=None, description="Historical and snapshot financials")
    news: Optional[NewsResearchResult] = Field(default=None, description="Authentic news research output")
    valuation: Optional[ValuationAnalysis] = Field(default=None, description="Quantitative valuation analysis")
    agent_status: dict[str, str] = Field(default_factory=dict, description="Execution status of LangGraph pipeline agents")
    errors: list[str] = Field(default_factory=list, description="Pipeline warnings or error logs")
