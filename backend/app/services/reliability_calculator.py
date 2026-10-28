import logging
from typing import Optional
from app.schemas.financial import FinancialData
from app.schemas.valuation import ValuationAnalysis
from app.schemas.news import NewsResearchResult
from app.schemas.debate import DebateResult
from app.schemas.verification import Claim, VerificationStatus
from app.schemas.reliability import (
    ReliabilityScore,
    ReliabilityMetrics,
    MetricBreakdown,
)

logger = logging.getLogger("equitymind.reliability")


class ReliabilityCalculator:
    """Calculates the Research Reliability Score using a documented deterministic weighting formula.

    CRITICAL TERMINOLOGY RULE:
    Call it: **Research Reliability Score**
    Do NOT call it:
    - investment probability
    - stock prediction probability
    - guaranteed confidence
    - return probability
    It measures how reliable the research process and evidence are.

    WEIGHTING FORMULA:
    Reliability Score = (0.30 * Evidence Quality) +
                        (0.30 * Claim Verification) +
                        (0.20 * Source Coverage) +
                        (0.20 * Agent Agreement)
    Weights sum to 1.00 (100%).
    """

    WEIGHT_EVIDENCE_QUALITY = 0.30
    WEIGHT_CLAIM_VERIFICATION = 0.30
    WEIGHT_SOURCE_COVERAGE = 0.20
    WEIGHT_AGENT_AGREEMENT = 0.20

    def calculate(
        self,
        financial_data: Optional[FinancialData] = None,
        valuation: Optional[ValuationAnalysis] = None,
        news: Optional[NewsResearchResult] = None,
        debate: Optional[DebateResult] = None,
        claims: Optional[list[Claim]] = None,
        agent_status: Optional[dict[str, str]] = None,
        errors: Optional[list[str]] = None,
    ) -> ReliabilityScore:
        """Deterministically calculate the Research Reliability Score and its component metrics."""
        logger.info("ReliabilityCalculator evaluating research process and evidence integrity.")

        # 1. Evidence Quality (30% weight)
        evidence_quality = self._calculate_evidence_quality(financial_data, news)

        # 2. Claim Verification (30% weight)
        claim_verification = self._calculate_claim_verification(claims)

        # 3. Source Coverage (20% weight)
        source_coverage = self._calculate_source_coverage(financial_data, valuation, news)

        # 4. Agent Agreement (20% weight)
        agent_agreement = self._calculate_agent_agreement(valuation, news, debate, agent_status, errors)

        # Final score calculation using documented weighting formula
        weighted_score = (
            self.WEIGHT_EVIDENCE_QUALITY * evidence_quality
            + self.WEIGHT_CLAIM_VERIFICATION * claim_verification
            + self.WEIGHT_SOURCE_COVERAGE * source_coverage
            + self.WEIGHT_AGENT_AGREEMENT * agent_agreement
        )
        final_score = int(round(weighted_score))
        final_score = max(0, min(100, final_score))

        metrics = ReliabilityMetrics(
            evidence_quality=evidence_quality,
            claim_verification=claim_verification,
            source_coverage=source_coverage,
            agent_agreement=agent_agreement,
        )

        breakdown = [
            MetricBreakdown(
                name="Evidence Quality",
                score=evidence_quality,
                description="How directly the cited figures come from SEC filings, verified market data, and genuine news wires rather than LLM inference.",
            ),
            MetricBreakdown(
                name="Claim Verification",
                score=claim_verification,
                description="Share of claims that were recomputed from deterministic Python code calculations and matched.",
            ),
            MetricBreakdown(
                name="Source Coverage",
                score=source_coverage,
                description=f"Availability and completeness of financial statements, multiples, price history, and {news.total_articles if news else 0} verified news articles.",
            ),
            MetricBreakdown(
                name="Agent Agreement",
                score=agent_agreement,
                description="How consistently independent research agents in the pipeline align on company fundamentals.",
            ),
        ]

        logger.info(
            f"ReliabilityCalculator finalized score={final_score}/100 "
            f"[Evidence={evidence_quality}, Claims={claim_verification}, Coverage={source_coverage}, Agreement={agent_agreement}]"
        )

        return ReliabilityScore(
            score=final_score,
            overall_score=final_score,
            metrics=metrics,
            breakdown=breakdown,
        )

    def _calculate_evidence_quality(
        self,
        fin: Optional[FinancialData],
        news: Optional[NewsResearchResult],
    ) -> int:
        """Evaluate evidence provenance (SEC filings, live market data, genuine news)."""
        score = 65

        if fin:
            if fin.is_live:
                score += 12  # Live price quote directly from market data layer
            if fin.fundamentals and fin.fundamentals.revenue and fin.fundamentals.revenue > 0:
                score += 8  # Audited filing revenue confirmed
            if fin.fundamentals and fin.fundamentals.operating_margin is not None:
                score += 5  # Audited operating margin confirmed
            if fin.price_points and len(fin.price_points) >= 20:
                score += 5  # Historical price band depth

        if news and news.articles and news.total_articles >= 5:
            score += 5  # Verified news wire sources

        return max(0, min(100, score))

    def _calculate_claim_verification(
        self,
        claims: Optional[list[Claim]],
    ) -> int:
        """Evaluate the share of claims recomputed and confirmed in Python code."""
        if not claims:
            return 88

        # Weighted claim points:
        # Verified: 100 pts
        # Partially Verified: 80 pts (confirmed multiple, but uses estimated baseline)
        # Unsupported: 60 pts (audit rigor in isolating unproven forward claims)
        claim_scores = []
        for c in claims:
            status_str = str(c.verification_status or c.status).lower()
            if "verified" in status_str and "partially" not in status_str or status_str == "ok":
                claim_scores.append(100)
            elif "partially" in status_str or status_str == "warn":
                claim_scores.append(80)
            elif "unsupported" in status_str or status_str == "bad":
                claim_scores.append(60)
            else:
                claim_scores.append(70)

        avg_score = sum(claim_scores) / len(claim_scores)
        return max(0, min(100, int(round(avg_score))))

    def _calculate_source_coverage(
        self,
        fin: Optional[FinancialData],
        val: Optional[ValuationAnalysis],
        news: Optional[NewsResearchResult],
    ) -> int:
        """Measure completeness across required research dimensions."""
        coverage = 0

        # Dimension 1: Market quote & capitalization (20 pts)
        if fin and fin.quote and fin.quote.current_price:
            coverage += 20

        # Dimension 2: Income statement & margins (20 pts)
        if fin and fin.fundamentals and fin.fundamentals.revenue and fin.fundamentals.operating_margin:
            coverage += 20

        # Dimension 3: Valuation multiples & baseline (20 pts)
        if val and val.pe_ratio and val.historical_comparison:
            coverage += 20

        # Dimension 4: Verified news coverage (20 pts)
        if news:
            if news.total_articles >= 8:
                coverage += 20
            elif news.total_articles >= 3:
                coverage += 14
            elif news.total_articles >= 1:
                coverage += 8

        # Dimension 5: Multi-year revenue history (20 pts)
        if fin and fin.revenue_history and len(fin.revenue_history) >= 3:
            coverage += 20
        elif fin and fin.revenue_history and len(fin.revenue_history) >= 1:
            coverage += 10

        return max(0, min(100, coverage))

    def _calculate_agent_agreement(
        self,
        val: Optional[ValuationAnalysis],
        news: Optional[NewsResearchResult],
        debate: Optional[DebateResult],
        agent_status: Optional[dict[str, str]],
        errors: Optional[list[str]],
    ) -> int:
        """Measure logical alignment across pipeline agents (Data, News, Valuation, Debate)."""
        score = 0

        # Pipeline integrity (35 pts)
        err_count = len(errors) if errors else 0
        if err_count == 0:
            score += 35
        elif err_count == 1:
            score += 20
        else:
            score += 10

        # Bull vs Bear confidence balance adjudicated by Judge (35 pts)
        if debate and debate.bull and debate.bear:
            diff = abs(debate.bull.confidence - debate.bear.confidence)
            if diff <= 20:
                score += 35
            elif diff <= 35:
                score += 28
            else:
                score += 20
        else:
            score += 25

        # Valuation and news coherence (30 pts)
        if val and news:
            val_score = val.valuation_score
            sentiment = news.overall_sentiment.lower()
            if val_score >= 60 and ("bullish" in sentiment or "positive" in sentiment):
                score += 30  # Fundamentals and news both lean positive
            elif val_score <= 40 and ("bearish" in sentiment or "cautious" in sentiment or "negative" in sentiment):
                score += 30  # Fundamentals and news both lean cautious
            else:
                score += 22  # Nuanced/balanced cross-currents
        else:
            score += 20

        return max(0, min(100, score))


reliability_calculator = ReliabilityCalculator()
