from typing import Optional, TypedDict, Annotated
from pydantic import BaseModel, Field
from app.schemas.company import Company
from app.schemas.financial import FinancialData
from app.schemas.news import NewsResearchResult
from app.schemas.valuation import ValuationAnalysis
from app.schemas.debate import DebateSide, DebateResult
from app.schemas.verification import Claim


def update_dict(existing: dict, new_val: dict) -> dict:
    """Reducer to merge agent statuses from parallel branches in LangGraph."""
    res = dict(existing or {})
    if new_val:
        res.update(new_val)
    return res


def add_list(existing: list, new_items: list) -> list:
    """Reducer to accumulate errors across parallel branches in LangGraph."""
    res = list(existing or [])
    if new_items:
        for item in new_items:
            if item not in res:
                res.append(item)
    return res


class ResearchState(TypedDict, total=False):
    """LangGraph shared research state with reducer annotations for parallel execution."""

    company: Company
    financial_data: Optional[FinancialData]
    news: Optional[NewsResearchResult]
    valuation: Optional[ValuationAnalysis]
    bull_case: Optional[DebateSide]
    bear_case: Optional[DebateSide]
    debate: Optional[DebateResult]
    claims: Optional[list[Claim]]
    agent_status: Annotated[dict[str, str], update_dict]
    errors: Annotated[list[str], add_list]


class ResearchStateModel(BaseModel):
    """Pydantic validated model representing the complete research state."""

    company: Company = Field(..., description="Target company under research")
    financial_data: Optional[FinancialData] = Field(
        default=None, description="Retrieved market data and financial metrics"
    )
    news: Optional[NewsResearchResult] = Field(
        default=None, description="Retrieved and summarized authentic news"
    )
    valuation: Optional[ValuationAnalysis] = Field(
        default=None, description="Computed valuation metrics and reasoning"
    )
    bull_case: Optional[DebateSide] = Field(
        default=None, description="Evidence-backed bull case"
    )
    bear_case: Optional[DebateSide] = Field(
        default=None, description="Adversarial evidence-backed bear case"
    )
    debate: Optional[DebateResult] = Field(
        default=None, description="Final adjudicated Bull vs Bear debate result"
    )
    claims: Optional[list[Claim]] = Field(
        default=None, description="Verified claims against source ground-truth data"
    )
    agent_status: dict[str, str] = Field(
        default_factory=lambda: {
            "data": "idle",
            "news": "idle",
            "valuation": "idle",
            "bull": "idle",
            "bear": "idle",
            "judge": "idle",
            "verification": "idle",
        },
        description="Execution status of each pipeline agent",
    )
    errors: list[str] = Field(
        default_factory=list, description="Accumulated pipeline errors or warnings"
    )
