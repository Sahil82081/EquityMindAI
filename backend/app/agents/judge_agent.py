import logging
from typing import Optional
from app.schemas.company import Company
from app.schemas.financial import FinancialData
from app.schemas.valuation import ValuationAnalysis
from app.schemas.debate import DebateSide, DebateResult, JudgeAdjudicationOutput
from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)


def _format_financial_summary(fin: Optional[FinancialData]) -> str:
    if not fin:
        return "Financial data pending or unavailable."
    q = fin.quote
    f = fin.fundamentals
    return (
        f"Price: {q.formatted_price} ({q.formatted_change}), Market Cap: {f.formatted_market_cap}, "
        f"Revenue: {f.formatted_revenue}, Net Income: {f.formatted_net_income}, "
        f"EPS: {f.formatted_eps}, Rev Growth: {f.formatted_revenue_growth}, "
        f"Operating Margin: {f.formatted_operating_margin}, Net Margin: {f.formatted_net_margin}, "
        f"Trailing P/E: {f.formatted_pe}"
    )


def _format_valuation_summary(val: Optional[ValuationAnalysis]) -> str:
    if not val:
        return "Valuation analysis pending or unavailable."
    bench = val.historical_comparison.historical_benchmark if val.historical_comparison else (val.pe_ratio.benchmark or "N/A")
    return (
        f"Classification: {val.valuation_classification}, Valuation Score: {val.valuation_score}/100, "
        f"P/E: {val.pe_ratio.formatted_value} (Historical Benchmark: {bench}), "
        f"Revenue Growth: {val.revenue_growth.formatted_value}"
    )


class JudgeAgent:
    """Agent objectively adjudicating the Bull vs Bear debate.

    Mandate:
    - Compare Bull arguments
    - Compare Bear arguments
    - Examine supporting evidence
    - Identify weaknesses
    - Determine which arguments are better supported
    - Produce a balanced conclusion (NOT simply pick Bull or Bear)
    """

    def __init__(self):
        self.llm = llm_service

    def run(
        self,
        company: Company,
        bull: DebateSide,
        bear: DebateSide,
        financial_data: Optional[FinancialData] = None,
        valuation: Optional[ValuationAnalysis] = None,
    ) -> DebateResult:
        """Adjudicate the debate and synthesize a balanced conclusion."""
        logger.info(f"JudgeAgent adjudicating debate for {company.name} ({company.ticker})")

        fin_summary = _format_financial_summary(financial_data)
        val_summary = _format_valuation_summary(valuation)

        try:
            adjudication: JudgeAdjudicationOutput = self.llm.adjudicate_debate(
                company_name=company.name,
                ticker=company.ticker,
                bull=bull,
                bear=bear,
                financial_summary=fin_summary,
                valuation_summary=val_summary,
            )

            result = DebateResult(
                bull=bull,
                bear=bear,
                judge_conclusion=adjudication.balanced_conclusion,
                adjudication_detail=adjudication,
            )

            logger.info(
                f"JudgeAgent completed balanced adjudication for {company.ticker}. "
                f"Bull strengths={len(adjudication.bull_strengths)}, "
                f"Bear strengths={len(adjudication.bear_strengths)}"
            )
            return result
        except Exception as e:
            logger.error(f"JudgeAgent encountered error for {company.ticker}: {e}")
            raise


judge_agent = JudgeAgent()
