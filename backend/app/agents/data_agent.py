from typing import Optional
from app.schemas.company import Company
from app.schemas.financial import FinancialData
from app.services.market_data import MarketDataService


class DataAgent:
    """
    DataAgent represents the first specialist agent in the EquityMind AI multi-agent pipeline.
    Responsible for deterministic extraction and structure validation of financial numbers
    directly from financial filings and market data exchanges via yfinance.
    
    Guarantees:
    - Never uses an LLM to invent financial numbers.
    - All financial metrics originate from verified market data.
    - Gracefully handles missing metrics without crashing.
    """

    def __init__(self, market_service: Optional[MarketDataService] = None):
        self.market_service = market_service or MarketDataService()

    def run(self, company: Company) -> FinancialData:
        """
        Execute market data collection for the target company.
        """
        ticker = company.ticker.strip().upper()
        financial_data = self.market_service.fetch_market_data(ticker)
        return financial_data


# Singleton agent instance
data_agent = DataAgent()
