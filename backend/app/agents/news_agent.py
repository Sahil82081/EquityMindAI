import logging
from app.schemas.company import Company
from app.schemas.news import NewsResearchResult
from app.services.news_service import news_service

logger = logging.getLogger(__name__)


class NewsAgent:
    """Agent responsible for gathering and synthesizing authentic company news.

    Strict rule: All articles and URLs originate from authentic news feeds;
    the LLM is never permitted to fabricate articles or URLs.
    """

    def __init__(self):
        self.service = news_service

    def run(self, company: Company, limit: int = 10) -> NewsResearchResult:
        """Collect and structure recent legitimate company news."""
        logger.info(f"NewsAgent analyzing company news for {company.name} ({company.ticker})")
        try:
            result = self.service.fetch_news(
                ticker=company.ticker,
                company_name=company.name,
                limit=limit,
            )
            logger.info(
                f"NewsAgent completed news research for {company.ticker}: "
                f"{result.total_articles} articles, sentiment: {result.overall_sentiment}"
            )
            return result
        except Exception as e:
            logger.error(f"NewsAgent encountered error for {company.ticker}: {e}")
            return NewsResearchResult(
                ticker=company.ticker,
                company_name=company.name,
                articles=[],
                overall_sentiment="neutral",
                positive_count=0,
                negative_count=0,
                neutral_count=0,
                total_articles=0,
                source_coverage="News feed temporarily unavailable",
            )


news_agent = NewsAgent()
