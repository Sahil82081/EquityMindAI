from typing import Optional
from pydantic import BaseModel, Field
from .gemini_outputs import ValuationReasoningOutput


class ValuationMetric(BaseModel):
    """Individual valuation metric with computed value, benchmark, and formula audit."""

    metric_name: str = Field(..., description="Name of the financial metric")
    value: Optional[float] = Field(default=None, description="Raw numerical value")
    formatted_value: str = Field(..., description="Display string e.g. '39.4x' or '+16.4%'")
    benchmark: Optional[str] = Field(default=None, description="Industry or historical reference benchmark")
    assessment: str = Field(..., description="Qualitative rating e.g. 'Elevated', 'Fair', 'Attractive'")
    calculation_formula: str = Field(..., description="Exact formula and inputs used to derive the metric")
    explanation: str = Field(..., description="Analytical explanation of what this metric implies")


class HistoricalValuationComparison(BaseModel):
    """Historical multiple and peer benchmark comparison."""

    metric: str = Field(default="P/E Multiple vs Historical Baseline", description="Comparison metric name")
    current_value: str = Field(..., description="Current multiple value e.g. '39.4x'")
    historical_benchmark: str = Field(..., description="Baseline reference multiple e.g. '5-Year Average: ~29.5x'")
    variance_percent: Optional[float] = Field(default=None, description="Percentage variance from historical baseline")
    historical_context: str = Field(..., description="Historical context summary e.g. 'Premium expansion of +33.6%'")
    comparison_summary: str = Field(..., description="Detailed narrative comparison against history and growth rate")


class ValuationAnalysis(BaseModel):
    """Complete quantitative and narrative valuation analysis."""

    ticker: str = Field(..., description="Company ticker symbol")
    company_name: str = Field(..., description="Company name")
    pe_ratio: ValuationMetric = Field(..., description="Trailing P/E metric")
    forward_pe: Optional[ValuationMetric] = Field(default=None, description="Forward P/E metric if available")
    revenue_growth: ValuationMetric = Field(..., description="Year-over-year revenue growth metric")
    operating_margin: ValuationMetric = Field(..., description="Operating margin metric")
    net_margin: ValuationMetric = Field(..., description="Net margin metric")
    historical_comparison: HistoricalValuationComparison = Field(..., description="Comparison with historical multiples")
    valuation_score: int = Field(..., ge=0, le=100, description="Composite valuation score out of 100")
    valuation_classification: str = Field(..., description="Overall classification e.g. 'Premium Valuation', 'Fairly Valued', 'Undervalued'")
    executive_explanation: str = Field(..., description="Executive narrative explaining the valuation numbers")
    calculations_summary: list[str] = Field(default_factory=list, description="List of all auditable mathematical formulas executed in code")
    reasoning: Optional[ValuationReasoningOutput] = Field(
        default=None, description="Gemini valuation reasoning validated with Pydantic"
    )
