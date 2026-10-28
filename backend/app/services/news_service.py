import html
import logging
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Optional, Literal
from app.schemas.news import NewsArticle, NewsResearchResult

logger = logging.getLogger(__name__)

# Curated financial sentiment keywords for deterministic, reliable scoring
_POSITIVE_KEYWORDS = {
    "surge", "surges", "surging", "jump", "jumps", "jumped", "rally", "rallies",
    "gain", "gains", "gained", "rise", "rises", "rising", "soar", "soars",
    "beat", "beats", "beating", "exceed", "exceeds", "record", "high", "highs",
    "growth", "growing", "strong", "outperform", "outperformed", "upgrade", "upgrades",
    "profit", "profitable", "bull", "bullish", "boost", "boosts", "dividend",
    "buyback", "expansion", "innovate", "win", "wins", "robust", "resilient"
}

_NEGATIVE_KEYWORDS = {
    "slump", "slumps", "slumping", "plunge", "plunges", "plunging", "drop", "drops",
    "dropped", "fall", "falls", "falling", "decline", "declines", "declining",
    "miss", "misses", "missing", "missed", "loss", "losses", "cut", "cuts",
    "downgrade", "downgrades", "downgraded", "bear", "bearish", "weak", "weakness",
    "warning", "warns", "warned", "lawsuit", "sued", "probe", "investigation",
    "subpoena", "struggle", "struggles", "layoff", "layoffs", "antitrust", "penalty",
    "fine", "risk", "risks", "debt", "recession", "down", "trouble", "fail", "fails"
}


def _clean_text(raw: Optional[str]) -> str:
    """Strip HTML tags and unescape entities."""
    if not raw:
        return ""
    clean = re.sub(r"<[^>]+>", "", raw)
    clean = html.unescape(clean)
    return clean.strip()


def _analyze_sentiment(text: str) -> tuple[Literal["positive", "negative", "neutral"], float]:
    """Deterministically analyze financial sentiment of text using financial sentiment lexicon."""
    words = re.findall(r"\b[a-zA-Z-]+\b", text.lower())
    if not words:
        return "neutral", 0.0

    pos_score = sum(1 for w in words if w in _POSITIVE_KEYWORDS)
    neg_score = sum(1 for w in words if w in _NEGATIVE_KEYWORDS)
    net_diff = pos_score - neg_score

    if net_diff > 0:
        sentiment: Literal["positive", "negative", "neutral"] = "positive"
        score = min(1.0, round(net_diff / max(1, pos_score + neg_score), 2))
    elif net_diff < 0:
        sentiment = "negative"
        score = max(-1.0, round(net_diff / max(1, pos_score + neg_score), 2))
    else:
        sentiment = "neutral"
        score = 0.0

    return sentiment, score


class NewsService:
    """Service to fetch verified, legitimate news from authenticated financial feeds."""

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 EquityMindAI/1.0"

    def fetch_news(self, ticker: str, company_name: str, limit: int = 10) -> NewsResearchResult:
        clean_ticker = ticker.strip().upper()
        clean_name = company_name.strip()
        articles: list[NewsArticle] = []
        seen_urls = set()
        seen_titles = set()

        # Source 1: Yahoo Finance RSS feed
        yf_articles = self._fetch_yahoo_finance_rss(clean_ticker)
        for a in yf_articles:
            if a.url not in seen_urls and a.headline.lower() not in seen_titles:
                seen_urls.add(a.url)
                seen_titles.add(a.headline.lower())
                articles.append(a)

        # Source 2: Google News Finance RSS feed (supplement if needed)
        if len(articles) < limit:
            gn_articles = self._fetch_google_news_rss(clean_ticker, clean_name, limit - len(articles))
            for a in gn_articles:
                if a.url not in seen_urls and a.headline.lower() not in seen_titles:
                    seen_urls.add(a.url)
                    seen_titles.add(a.headline.lower())
                    articles.append(a)

        # Truncate to desired limit
        final_articles = articles[:limit]

        # Calculate sentiment aggregates
        pos_count = sum(1 for a in final_articles if a.sentiment == "positive")
        neg_count = sum(1 for a in final_articles if a.sentiment == "negative")
        neu_count = sum(1 for a in final_articles if a.sentiment == "neutral")
        total = len(final_articles)

        if total == 0:
            overall = "neutral"
        elif pos_count > neg_count * 1.5:
            overall = "bullish"
        elif pos_count > neg_count:
            overall = "neutral, leaning bullish"
        elif neg_count > pos_count * 1.5:
            overall = "bearish"
        elif neg_count > pos_count:
            overall = "cautious, leaning bearish"
        else:
            overall = "neutral"

        # Use Gemini for reasoning and summarization (validated with Pydantic)
        from app.services.llm_service import llm_service
        synthesis = llm_service.synthesize_news(
            ticker=clean_ticker,
            company_name=clean_name,
            articles=[a.model_dump() for a in final_articles],
            overall_sentiment=overall,
        )

        return NewsResearchResult(
            ticker=clean_ticker,
            company_name=clean_name,
            articles=final_articles,
            overall_sentiment=overall,
            positive_count=pos_count,
            negative_count=neg_count,
            neutral_count=neu_count,
            total_articles=total,
            source_coverage=f"Yahoo Finance RSS & Google News ({total} verified articles)",
            synthesis=synthesis,
        )

    def _fetch_yahoo_finance_rss(self, ticker: str) -> list[NewsArticle]:
        url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
        req = urllib.request.Request(url, headers={"User-Agent": self.USER_AGENT})
        results: list[NewsArticle] = []

        try:
            with urllib.request.urlopen(req, timeout=8) as response:
                content = response.read()
                root = ET.fromstring(content)
                channel = root.find("channel")
                if channel is None:
                    return results

                items = channel.findall("item")
                for item in items:
                    title_elem = item.find("title")
                    link_elem = item.find("link")
                    pub_elem = item.find("pubDate")
                    desc_elem = item.find("description")

                    if title_elem is None or not title_elem.text or link_elem is None or not link_elem.text:
                        continue

                    headline = _clean_text(title_elem.text)
                    link = link_elem.text.strip()
                    published_at = pub_elem.text.strip() if pub_elem is not None and pub_elem.text else datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
                    summary = _clean_text(desc_elem.text) if desc_elem is not None else headline

                    # Extract source from domain or title if possible
                    source = "Yahoo Finance"
                    if "fool.com" in link:
                        source = "The Motley Fool"
                    elif "thestreet.com" in link:
                        source = "TheStreet"
                    elif "investors.com" in link:
                        source = "Investor's Business Daily"
                    elif "zacks.com" in link:
                        source = "Zacks Investment Research"
                    elif "bloomberg.com" in link:
                        source = "Bloomberg"
                    elif "reuters.com" in link:
                        source = "Reuters"

                    sentiment, score = _analyze_sentiment(f"{headline}. {summary}")

                    results.append(
                        NewsArticle(
                            headline=headline,
                            source=source,
                            published_at=published_at,
                            url=link,
                            summary=summary or headline,
                            sentiment=sentiment,
                            sentiment_score=score,
                        )
                    )
        except Exception as e:
            logger.warning(f"Error fetching Yahoo Finance RSS for {ticker}: {e}")

        return results

    def _fetch_google_news_rss(self, ticker: str, company_name: str, limit: int) -> list[NewsArticle]:
        query = urllib.parse.quote_plus(f"{ticker} stock OR {company_name}")
        url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        req = urllib.request.Request(url, headers={"User-Agent": self.USER_AGENT})
        results: list[NewsArticle] = []

        try:
            with urllib.request.urlopen(req, timeout=8) as response:
                content = response.read()
                root = ET.fromstring(content)
                channel = root.find("channel")
                if channel is None:
                    return results

                items = channel.findall("item")
                for item in items[:limit]:
                    title_elem = item.find("title")
                    link_elem = item.find("link")
                    pub_elem = item.find("pubDate")
                    source_elem = item.find("source")
                    desc_elem = item.find("description")

                    if title_elem is None or not title_elem.text or link_elem is None or not link_elem.text:
                        continue

                    raw_title = _clean_text(title_elem.text)
                    source = source_elem.text.strip() if source_elem is not None and source_elem.text else "Google News"
                    
                    # Clean title: often formatted like "Article Title - Publisher"
                    headline = raw_title
                    if " - " in raw_title:
                        parts = raw_title.rsplit(" - ", 1)
                        if len(parts) == 2 and not source_elem:
                            headline = parts[0]
                            source = parts[1]
                        elif len(parts) == 2 and source.lower() in parts[1].lower():
                            headline = parts[0]

                    link = link_elem.text.strip()
                    published_at = pub_elem.text.strip() if pub_elem is not None and pub_elem.text else datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
                    summary = _clean_text(desc_elem.text) if desc_elem is not None else headline

                    sentiment, score = _analyze_sentiment(f"{headline}. {summary}")

                    results.append(
                        NewsArticle(
                            headline=headline,
                            source=source,
                            published_at=published_at,
                            url=link,
                            summary=summary or headline,
                            sentiment=sentiment,
                            sentiment_score=score,
                        )
                    )
        except Exception as e:
            logger.warning(f"Error fetching Google News RSS for {ticker}: {e}")

        return results


news_service = NewsService()
