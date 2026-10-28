import logging
from app.schemas.company import Company
from app.schemas.financial import FinancialData
from app.schemas.valuation import ValuationAnalysis
from app.services.valuation_calculator import valuation_calculator

logger = logging.getLogger(__name__)


class ValuationAgent:
    """Agent performing rigorous quantitative valuation analysis and multiple comparison.

    Rule: All calculations (P/E, revenue growth, operating margin, net margin,
    historical comparisons) are executed in pure Python code.
    Gemini or narrative generation strictly explains verified computed numbers without fabricating figures.
    """

    def __init__(self):
        self.calculator = valuation_calculator

    def run(self, company: Company, financial_data: FinancialData) -> ValuationAnalysis:
        """Run valuation analysis on verified company financial data."""
        logger.info(f"ValuationAgent computing valuation metrics for {company.name} ({company.ticker})")
        try:
            analysis = self.calculator.analyze(
                ticker=company.ticker,
                company_name=company.name,
                fin=financial_data,
            )
            logger.info(
                f"ValuationAgent completed analysis for {company.ticker}: "
                f"P/E={analysis.pe_ratio.formatted_value}, "
                f"RevGrowth={analysis.revenue_growth.formatted_value}, "
                f"Score={analysis.valuation_score}/100, "
                f"Classification={analysis.valuation_classification}"
            )
            return analysis
        except Exception as e:
            logger.error(f"ValuationAgent encountered error for {company.ticker}: {e}")
            raise


valuation_agent = ValuationAgent()
