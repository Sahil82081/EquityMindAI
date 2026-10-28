import logging
from typing import Optional
from app.schemas.company import Company
from app.schemas.financial import FinancialData
from app.schemas.valuation import ValuationAnalysis
from app.schemas.news import NewsResearchResult
from app.schemas.debate import DebateSide
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
    summary = ""
    if val.reasoning and getattr(val.reasoning, "executive_summary", None):
        summary = val.reasoning.executive_summary[:200]
    elif val.executive_explanation:
        summary = val.executive_explanation[:200]
    return (
        f"Classification: {val.valuation_classification}, Valuation Score: {val.valuation_score}/100, "
        f"P/E: {val.pe_ratio.formatted_value} (Historical Benchmark: {bench}), "
        f"Revenue Growth: {val.revenue_growth.formatted_value}, "
        f"Summary: {summary}..."
    )


def _format_news_summary(news: Optional[NewsResearchResult]) -> str:
    if not news or not news.articles:
        return "News sentiment neutral / no major breaking coverage."
    headlines = "; ".join([f"'{a.headline}'" for a in news.articles[:3]])
    return (
        f"Overall Sentiment: {news.overall_sentiment} ({news.positive_count} positive, "
        f"{news.negative_count} negative, {news.neutral_count} neutral). Recent: {headlines}"
    )


def _format_bull_arguments(bull: Optional[DebateSide]) -> str:
    if not bull or not bull.arguments:
        return "Bull thesis centers on scale, margin resilience, and competitive franchise moat."
    return "\n".join([f"- {arg.title}: {arg.description} ({arg.source})" for arg in bull.arguments])


class BearAgent:
    """Agent building the strongest evidence-backed bearish case actively challenging the Bull thesis."""

    def __init__(self):
        self.llm = llm_service

    def run(
        self,
        company: Company,
        financial_data: Optional[FinancialData] = None,
        valuation: Optional[ValuationAnalysis] = None,
        news: Optional[NewsResearchResult] = None,
        bull_case: Optional[DebateSide] = None,
    ) -> DebateSide:
        """Execute Bear Agent research to actively contest the Bull thesis using shared state."""
        logger.info(f"BearAgent constructing adversarial bearish case for {company.name} ({company.ticker})")

        fin_summary = _format_financial_summary(financial_data)
        val_summary = _format_valuation_summary(valuation)
        news_summary = _format_news_summary(news)
        bull_summary = _format_bull_arguments(bull_case)

        try:
            bear_case = self.llm.generate_bear_case(
                company_name=company.name,
                ticker=company.ticker,
                financial_summary=fin_summary,
                valuation_summary=val_summary,
                news_summary=news_summary,
                bull_arguments_summary=bull_summary,
            )
            logger.info(
                f"BearAgent completed thesis for {company.ticker}: "
                f"Confidence={bear_case.confidence}%, Arguments={len(bear_case.arguments)}"
            )
            return bear_case
        except Exception as e:
            logger.error(f"BearAgent encountered error for {company.ticker}: {e}")
            raise


bear_agent = BearAgent()
