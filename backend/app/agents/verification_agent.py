import logging
from typing import Optional
from app.schemas.company import Company
from app.schemas.financial import FinancialData
from app.schemas.valuation import ValuationAnalysis
from app.schemas.news import NewsResearchResult
from app.schemas.debate import DebateResult
from app.schemas.verification import Claim
from app.services.claim_verifier import claim_verifier

logger = logging.getLogger(__name__)


class VerificationAgent:
    """Agent responsible for checking generated research claims against actual source data.

    Rules:
    - Never let LLM decide verification purely by itself.
    - Retrieve structured source values directly from financial data, filings, and news.
    - Perform calculations strictly in Python code.
    - Compare claims against source numbers with numerical tolerance.
    """

    def __init__(self):
        self.verifier = claim_verifier

    def run(
        self,
        company: Company,
        financial_data: Optional[FinancialData] = None,
        valuation: Optional[ValuationAnalysis] = None,
        news: Optional[NewsResearchResult] = None,
        debate: Optional[DebateResult] = None,
    ) -> list[Claim]:
        """Execute factual claim extraction, evidence retrieval, python calculation, and verification."""
        logger.info(f"VerificationAgent auditing research claims for {company.name} ({company.ticker})")
        try:
            claims = self.verifier.verify_claims(
                company=company,
                financial_data=financial_data,
                valuation=valuation,
                news=news,
                debate=debate,
            )
            logger.info(
                f"VerificationAgent completed verification for {company.ticker}: "
                f"{len(claims)} claims audited."
            )
            return claims
        except Exception as e:
            logger.error(f"VerificationAgent encountered error for {company.ticker}: {e}")
            raise


verification_agent = VerificationAgent()
