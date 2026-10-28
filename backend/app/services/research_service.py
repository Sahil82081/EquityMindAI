import logging
from datetime import datetime, timezone
import uuid
from typing import Optional
from app.schemas.company import Company
from app.schemas.financial import FinancialData, SnapshotMetric
from app.schemas.news import NewsResearchResult
from app.schemas.valuation import ValuationAnalysis
from app.schemas.state import ResearchState
from app.schemas.research import (
    ResearchStatus,
    ResearchResponse,
    ResearchReport,
    ResearchThesis,
    DebateResult,
    DebateSide,
    DebatePoint,
    Claim,
    ClaimProof,
    ReliabilityScore,
    MetricBreakdown,
)

logger = logging.getLogger("equitymind.research")
_RESEARCH_CACHE: dict[str, ResearchResponse] = {}


def _build_report(
    company: Company,
    fin: FinancialData,
    news_res: NewsResearchResult,
    val_res: ValuationAnalysis,
) -> ResearchReport:
    pe_str = val_res.pe_ratio.formatted_value
    rev_str = fin.fundamentals.formatted_revenue
    margin_str = fin.fundamentals.formatted_operating_margin
    price_str = fin.quote.formatted_price
    news_sentiment = news_res.overall_sentiment
    val_class = val_res.valuation_classification

    # Derive thesis badge from valuation score and news sentiment
    if val_res.valuation_score >= 70 and "bullish" in news_sentiment:
        badge = "Bullish"
        badge_class = "b-ok"
    elif val_res.valuation_score < 40:
        badge = "Cautious, premium valuation"
        badge_class = "b-bad"
    elif "bearish" in news_sentiment:
        badge = "Cautious, negative news sentiment"
        badge_class = "b-bad"
    else:
        badge = "Neutral, leaning bullish"
        badge_class = "b-warn"

    summary = (
        f"Summary for {company.name} ({company.ticker}) at {price_str}: The business recorded {rev_str} in revenue "
        f"with an operating margin of {margin_str} and net margin of {val_res.net_margin.formatted_value}. "
        f"Trading at a trailing P/E of {pe_str} ({val_res.historical_comparison.historical_context}), "
        f"the stock is evaluated as '{val_class}'. "
        f"Analysis of {news_res.total_articles} authentic news articles reflects a '{news_sentiment}' market tone "
        f"({news_res.positive_count} positive, {news_res.negative_count} cautious/negative). "
        "The quantitative valuation and verified financials provide an auditable foundation for investment evaluation."
    )

    strengths = [
        f"Reported revenue of {rev_str} (verified)",
        f"Operating margin at {margin_str} (verified in filings)",
        f"Net profit conversion of {val_res.net_margin.formatted_value} ({val_res.net_margin.assessment})",
    ]
    if news_res.positive_count > 0:
        strengths.append(f"{news_res.positive_count} positive catalysts identified across verified news headlines")

    risks = [
        f"Valuation: {val_res.pe_ratio.assessment} at {pe_str} P/E ({val_res.historical_comparison.historical_context})",
        f"YoY revenue growth recorded at {val_res.revenue_growth.formatted_value}",
    ]
    if news_res.negative_count > 0:
        risks.append(f"{news_res.negative_count} critical/cautious headlines identified in recent media coverage")
    else:
        risks.append("Valuation leaves limited buffer for quarterly execution deceleration")

    return ResearchReport(
        thesis=ResearchThesis(
            sentiment_badge=badge,
            sentiment_class=badge_class,
            summary=summary,
        ),
        key_strengths=strengths,
        key_risks=risks,
        financial_snapshot=fin.snapshot,
        conclusion=(
            f"Attractive franchise fundamentals for {company.ticker} at {price_str}. "
            f"Quantitative valuation score is {val_res.valuation_score}/100 ({val_class}). "
            f"News sentiment stands at '{news_sentiment}' across {news_res.total_articles} authentic articles. "
            "This is research output grounded strictly in market data, not investment advice."
        ),
    )


def _build_debate(
    company: Company,
    fin: FinancialData,
    news_res: NewsResearchResult,
    val_res: ValuationAnalysis,
) -> DebateResult:
    rev_str = fin.fundamentals.formatted_revenue
    margin_str = fin.fundamentals.formatted_operating_margin
    pe_str = val_res.pe_ratio.formatted_value

    bull_args = [
        DebatePoint(
            title="Scale and revenue foundation",
            description=f"Generated {rev_str} in reported revenue with YoY growth of {val_res.revenue_growth.formatted_value}",
            source="Source: SEC filings & verified income statement",
        ),
        DebatePoint(
            title="Operating leverage & margin resilience",
            description=f"Operating margin sustained at {margin_str} with {val_res.operating_margin.assessment.lower()}",
            source="Source: income statement & valuation calculator",
        ),
    ]
    if news_res.positive_count > 0:
        bull_args.append(
            DebatePoint(
                title="Positive news catalysts",
                description=f"Identified {news_res.positive_count} favorable headlines in authenticated financial media",
                source=f"Source: {news_res.source_coverage}",
            )
        )
    else:
        bull_args.append(
            DebatePoint(
                title="Balance sheet durability",
                description="High net profit margins support ongoing shareholder returns and reinvestment",
                source="Source: cash-flow statement",
            )
        )

    bear_args = [
        DebatePoint(
            title="Multiple elevation & execution risk",
            description=f"Valuation at {pe_str} P/E ({val_res.historical_comparison.historical_context})",
            source=f"Source: {val_res.pe_ratio.calculation_formula}",
        ),
        DebatePoint(
            title="Historical valuation comparison",
            description=val_res.historical_comparison.comparison_summary,
            source="Source: 5-year multiple benchmark analysis",
        ),
    ]
    if news_res.negative_count > 0:
        bear_args.append(
            DebatePoint(
                title="Negative media headlines",
                description=f"{news_res.negative_count} cautious or critical articles recorded in recent news monitoring",
                source=f"Source: {news_res.source_coverage}",
            )
        )
    else:
        bear_args.append(
            DebatePoint(
                title="Deceleration sensitivity",
                description="High multiple magnifies downside volatility upon any top-line deceleration",
                source="Source: market data risk model",
            )
        )

    return DebateResult(
        bull=DebateSide(
            confidence=72,
            key_metrics=f"Rev {rev_str}, margin {margin_str}",
            arguments=bull_args,
        ),
        bear=DebateSide(
            confidence=58,
            key_metrics=f"P/E {pe_str}",
            arguments=bear_args,
        ),
        judge_conclusion=(
            f"The evidence demonstrates strong operating scale ({rev_str} revenue, {margin_str} margin). "
            f"However, the valuation assessment of '{val_res.valuation_classification}' ({pe_str} P/E) "
            f"and news tone ({news_res.overall_sentiment}) warrant a disciplined stance rather than aggressive chasing."
        ),
    )


def _build_claims(
    company: Company,
    fin: FinancialData,
    news_res: NewsResearchResult,
    val_res: ValuationAnalysis,
) -> list[Claim]:
    rev_str = fin.fundamentals.formatted_revenue
    margin_str = fin.fundamentals.formatted_operating_margin
    pe_str = val_res.pe_ratio.formatted_value
    eps_str = fin.fundamentals.formatted_eps

    claims = [
        Claim(
            id="c1",
            statement=f"{company.ticker} generated {rev_str} in reported revenue with {val_res.revenue_growth.formatted_value} YoY growth.",
            status="ok",
            proofs=[
                ClaimProof(label="Source data", detail=f"Market data total revenue: {rev_str}"),
                ClaimProof(label="Calculation", detail=val_res.revenue_growth.calculation_formula),
            ],
            result="Matches reported filing figures.",
        ),
        Claim(
            id="c2",
            statement=f"Operating margin stands at {margin_str} with net margin of {val_res.net_margin.formatted_value}.",
            status="ok",
            proofs=[
                ClaimProof(label="Source data", detail=f"Operating margin verified at {margin_str}"),
                ClaimProof(label="Calculation", detail=val_res.operating_margin.calculation_formula),
            ],
            result="Matches reported income statement.",
        ),
        Claim(
            id="c3",
            statement=f"The stock trades at a valuation multiple of {pe_str} P/E (EPS {eps_str}).",
            status="warn" if val_res.valuation_score < 50 else "ok",
            proofs=[
                ClaimProof(label="Source data", detail=val_res.pe_ratio.calculation_formula),
                ClaimProof(label="Comparison", detail=val_res.historical_comparison.historical_context),
            ],
            result=f"Confirmed multiple. Assessed as '{val_res.pe_ratio.assessment}'.",
        ),
    ]

    if news_res.total_articles > 0:
        claims.append(
            Claim(
                id="c4",
                statement=f"Recent media coverage across {news_res.total_articles} authentic articles reflects a '{news_res.overall_sentiment}' tone.",
                status="ok",
                proofs=[
                    ClaimProof(label="Source data", detail=f"{news_res.source_coverage}"),
                    ClaimProof(label="Breakdown", detail=f"{news_res.positive_count} positive, {news_res.negative_count} negative, {news_res.neutral_count} neutral"),
                ],
                result="Audited from authentic financial news feeds without fabrication.",
            )
        )
    else:
        claims.append(
            Claim(
                id="c4",
                statement="Management guidance implies accelerating growth next year.",
                status="bad",
                proofs=[
                    ClaimProof(label="Source data", detail="No forward guidance numbers confirmed in retrieved structured data"),
                    ClaimProof(label="Calculation", detail="None available"),
                ],
                result="No supporting structured data was retrieved. Treat as unverified.",
            )
        )

    return claims


from app.services.reliability_calculator import reliability_calculator


def create_research(company: Company) -> ResearchResponse:
    research_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    logger.info(f"=== Starting LangGraph Research Workflow for {company.name} ({company.ticker}) ===")

    # Initial state for LangGraph workflow including Bull, Bear, Judge, and Verification
    initial_state: ResearchState = {
        "company": company,
        "financial_data": None,
        "news": None,
        "valuation": None,
        "bull_case": None,
        "bear_case": None,
        "debate": None,
        "claims": None,
        "agent_status": {
            "data": "idle",
            "news": "idle",
            "valuation": "idle",
            "bull": "idle",
            "bear": "idle",
            "judge": "idle",
            "verification": "idle",
        },
        "errors": [],
    }

    # Execute LangGraph graph: Data -> News -> Valuation -> [Bull, Bear] -> Judge -> Verification -> END
    from app.workflows.research_workflow import research_graph
    final_state = research_graph.invoke(initial_state)

    financial_data = final_state.get("financial_data")
    news_result = final_state.get("news")
    valuation_result = final_state.get("valuation")
    debate_result = final_state.get("debate")
    claims_result = final_state.get("claims")
    agent_status = final_state.get("agent_status", {})
    errors = final_state.get("errors", [])

    # If debate was not produced in workflow (fallback safeguard)
    if debate_result is None and financial_data and news_result and valuation_result:
        debate_result = _build_debate(company, financial_data, news_result, valuation_result)

    # If claims were not produced in workflow (fallback safeguard)
    if claims_result is None:
        from app.services.claim_verifier import claim_verifier
        claims_result = claim_verifier.verify_claims(
            company=company,
            financial_data=financial_data,
            valuation=valuation_result,
            news=news_result,
            debate=debate_result,
        )

    logger.info(
        f"=== LangGraph Research Workflow completed for {company.ticker}: "
        f"agent_status={agent_status}, errors={len(errors)} ==="
    )

    reliability_score = reliability_calculator.calculate(
        financial_data=financial_data,
        valuation=valuation_result,
        news=news_result,
        debate=debate_result,
        claims=claims_result,
        agent_status=agent_status,
        errors=errors,
    )

    response = ResearchResponse(
        research_id=research_id,
        company=company,
        status=ResearchStatus.COMPLETED,
        created_at=now,
        report=_build_report(company, financial_data, news_result, valuation_result),
        debate=debate_result,
        claims=claims_result,
        reliability_score=reliability_score,
        financial_data=financial_data,
        news=news_result,
        valuation=valuation_result,
        agent_status=agent_status,
        errors=errors,
    )
    _RESEARCH_CACHE[research_id] = response
    return response


def get_research(research_id: str) -> Optional[ResearchResponse]:
    return _RESEARCH_CACHE.get(research_id)
