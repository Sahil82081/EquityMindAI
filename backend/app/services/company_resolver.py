import re
from dataclasses import dataclass
from typing import Optional
from app.schemas.company import Company, CompanySearchResponse


@dataclass(frozen=True)
class CompanyRecord:
    name: str
    ticker: str
    exchange: str
    market: str
    sector: Optional[str] = None
    aliases: tuple[str, ...] = ()

    def to_schema(self) -> Company:
        return Company(
            name=self.name,
            ticker=self.ticker,
            exchange=self.exchange,
            market=self.market,
            sector=self.sector,
        )


COMPANY_DATABASE: list[CompanyRecord] = [
    CompanyRecord(
        name="Apple Inc.",
        ticker="AAPL",
        exchange="NASDAQ",
        market="US",
        sector="Technology",
        aliases=("Apple", "Apple Computer"),
    ),
    CompanyRecord(
        name="Apple Hospitality REIT, Inc.",
        ticker="APLE",
        exchange="NYSE",
        market="US",
        sector="Real Estate",
        aliases=("Apple Hospitality",),
    ),
    CompanyRecord(
        name="Apple Rush Company",
        ticker="APRU",
        exchange="OTC",
        market="US",
        sector="Beverages",
        aliases=("Apple Rush",),
    ),
    CompanyRecord(
        name="Microsoft Corporation",
        ticker="MSFT",
        exchange="NASDAQ",
        market="US",
        sector="Technology",
        aliases=("Microsoft", "MS"),
    ),
    CompanyRecord(
        name="NVIDIA Corporation",
        ticker="NVDA",
        exchange="NASDAQ",
        market="US",
        sector="Technology",
        aliases=("Nvidia", "NVIDIA"),
    ),
    CompanyRecord(
        name="Tesla, Inc.",
        ticker="TSLA",
        exchange="NASDAQ",
        market="US",
        sector="Automotive",
        aliases=("Tesla", "Tesla Motors"),
    ),
    CompanyRecord(
        name="Amazon.com, Inc.",
        ticker="AMZN",
        exchange="NASDAQ",
        market="US",
        sector="Consumer Cyclical",
        aliases=("Amazon",),
    ),
    CompanyRecord(
        name="Alphabet Inc.",
        ticker="GOOGL",
        exchange="NASDAQ",
        market="US",
        sector="Communication Services",
        aliases=("Google", "Alphabet"),
    ),
    CompanyRecord(
        name="Meta Platforms, Inc.",
        ticker="META",
        exchange="NASDAQ",
        market="US",
        sector="Communication Services",
        aliases=("Meta", "Facebook", "FB"),
    ),
    CompanyRecord(
        name="Netflix, Inc.",
        ticker="NFLX",
        exchange="NASDAQ",
        market="US",
        sector="Communication Services",
        aliases=("Netflix",),
    ),
    CompanyRecord(
        name="Advanced Micro Devices, Inc.",
        ticker="AMD",
        exchange="NASDAQ",
        market="US",
        sector="Technology",
        aliases=("AMD",),
    ),
    CompanyRecord(
        name="Taiwan Semiconductor Manufacturing",
        ticker="TSM",
        exchange="NYSE",
        market="Taiwan",
        sector="Technology",
        aliases=("TSMC", "Taiwan Semiconductor"),
    ),
    CompanyRecord(
        name="Toyota Motor Corporation",
        ticker="TM",
        exchange="NYSE",
        market="Japan",
        sector="Automotive",
        aliases=("Toyota",),
    ),
    CompanyRecord(
        name="Intel Corporation",
        ticker="INTC",
        exchange="NASDAQ",
        market="US",
        sector="Technology",
        aliases=("Intel",),
    ),
    CompanyRecord(
        name="JPMorgan Chase & Co.",
        ticker="JPM",
        exchange="NYSE",
        market="US",
        sector="Financial Services",
        aliases=("JPMorgan", "Chase"),
    ),
    CompanyRecord(
        name="Tata Consultancy Services Limited",
        ticker="TCS.NS",
        exchange="NSE",
        market="India",
        sector="Technology",
        aliases=("TCS", "Tata Consultancy", "Tata Consultancy Services", "Tata"),
    ),
    CompanyRecord(
        name="Infosys Limited",
        ticker="INFY",
        exchange="NYSE",
        market="India",
        sector="Technology",
        aliases=("Infosys", "INFY.NS"),
    ),
    CompanyRecord(
        name="Reliance Industries Limited",
        ticker="RELIANCE.NS",
        exchange="NSE",
        market="India",
        sector="Energy & Conglomerate",
        aliases=("Reliance", "Reliance Industries", "RIL"),
    ),
    CompanyRecord(
        name="HDFC Bank Limited",
        ticker="HDB",
        exchange="NYSE",
        market="India",
        sector="Financial Services",
        aliases=("HDFC", "HDFC Bank", "HDFCBANK.NS"),
    ),
    CompanyRecord(
        name="ICICI Bank Limited",
        ticker="IBN",
        exchange="NYSE",
        market="India",
        sector="Financial Services",
        aliases=("ICICI", "ICICI Bank", "ICICIBANK.NS"),
    ),
    CompanyRecord(
        name="Wipro Limited",
        ticker="WIT",
        exchange="NYSE",
        market="India",
        sector="Technology",
        aliases=("Wipro", "WIPRO.NS"),
    ),
    CompanyRecord(
        name="Tata Motors Limited",
        ticker="TATAMOTORS.NS",
        exchange="NSE",
        market="India",
        sector="Automotive",
        aliases=("Tata Motors", "Tata"),
    ),
    CompanyRecord(
        name="State Bank of India",
        ticker="SBIN.NS",
        exchange="NSE",
        market="India",
        sector="Financial Services",
        aliases=("SBI", "State Bank of India"),
    ),
    CompanyRecord(
        name="Berkshire Hathaway Inc.",
        ticker="BRK-B",
        exchange="NYSE",
        market="US",
        sector="Financial Services",
        aliases=("Berkshire", "Berkshire Hathaway"),
    ),
]


class CompanyResolver:
    """
    Deterministic, rule-based company resolver.
    Does NOT use an LLM. Resolves company search queries via exact match,
    prefix match, tokenized keyword match, and Levenshtein edit distance.
    """

    def __init__(self, records: Optional[list[CompanyRecord]] = None):
        self.records = records if records is not None else COMPANY_DATABASE

    @staticmethod
    def normalize_text(text: str) -> str:
        """Strip punctuation, lowercase, and collapse excess whitespace."""
        cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
        return " ".join(cleaned.split()).strip()

    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        """Compute standard Levenshtein distance between two strings."""
        if s1 == s2:
            return 0
        if not s1:
            return len(s2)
        if not s2:
            return len(s1)

        dp = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1, 1):
            prev = dp[0]
            dp[0] = i
            for j, c2 in enumerate(s2, 1):
                temp = dp[j]
                cost = 0 if c1 == c2 else 1
                dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + cost)
                prev = temp
        return dp[-1]

    def resolve(self, query: str) -> CompanySearchResponse:
        """
        Deterministically resolve user query to normalized company results.
        Handles:
        - Exact ticker (e.g. AAPL)
        - Exact company name or alias (e.g. Apple, Google, Microsoft)
        - Partial company name or ticker (e.g. appl, micr, nvda)
        - Typos & spelling mistakes (e.g. Microsft, Appel, Nvdia, Tesal)
        - Ambiguous multi-matches (e.g. Apple -> Apple Inc., Apple Hospitality, Apple Rush)
        - No results (e.g. xyz12345)
        """
        raw_query = query.strip()
        norm_query = self.normalize_text(query)

        if not norm_query:
            return CompanySearchResponse(
                query=raw_query,
                results=[],
                fuzzy=False,
                ambiguous=False,
                count=0,
                match=None,
            )

        # ----------------------------------------------------
        # Stage 1: Exact Ticker Matching
        # ----------------------------------------------------
        exact_ticker_matches = [
            r for r in self.records
            if r.ticker.lower() == norm_query
            or r.ticker.lower().split(".")[0] == norm_query
            or any(self.normalize_text(a) == norm_query for a in r.aliases if len(a) <= 5)
        ]
        if exact_ticker_matches:
            companies = [r.to_schema() for r in exact_ticker_matches]
            return CompanySearchResponse(
                query=raw_query,
                results=companies,
                fuzzy=False,
                ambiguous=len(companies) > 1,
                count=len(companies),
                match=companies[0],
            )

        # ----------------------------------------------------
        # Stage 2: Direct Scoring (Prefix, Name, Alias, Substring)
        # ----------------------------------------------------
        scored_candidates: list[tuple[CompanyRecord, int]] = []

        for record in self.records:
            norm_name = self.normalize_text(record.name)
            ticker_lower = record.ticker.lower()
            norm_aliases = [self.normalize_text(a) for a in record.aliases]
            name_words = norm_name.split()

            score = 0

            # 1. Exact alias match (e.g. "Google" -> Alphabet Inc.)
            if any(a == norm_query for a in norm_aliases):
                score = 98
            # 2. Exact full company name match
            elif norm_name == norm_query:
                score = 95
            # 3. Company name starts with query (e.g. "Apple" starts with "app")
            elif norm_name.startswith(norm_query):
                score = 90
            # 4. Ticker starts with query (e.g. "AAP" -> AAPL)
            elif ticker_lower.startswith(norm_query):
                score = 85
            # 5. Any word in the company name starts with query
            elif any(w.startswith(norm_query) for w in name_words):
                score = 80
            # 6. Any alias starts with query
            elif any(a.startswith(norm_query) for a in norm_aliases):
                score = 75
            # 7. Substring in name
            elif norm_query in norm_name:
                score = 65

            if score > 0:
                scored_candidates.append((record, score))

        if scored_candidates:
            # Deterministic sorting: highest score first, then ticker alphabet order
            scored_candidates.sort(key=lambda item: (-item[1], item[0].ticker))
            top_results = [r.to_schema() for r, _ in scored_candidates[:6]]
            return CompanySearchResponse(
                query=raw_query,
                results=top_results,
                fuzzy=False,
                ambiguous=len(top_results) > 1,
                count=len(top_results),
                match=top_results[0],
            )

        # ----------------------------------------------------
        # Stage 3: Fuzzy / Typo Resolution (Minor spelling mistakes)
        # ----------------------------------------------------
        if len(norm_query) < 3:
            return CompanySearchResponse(
                query=raw_query,
                results=[],
                fuzzy=False,
                ambiguous=False,
                count=0,
                match=None,
            )

        # Allow max 1 edit for 3-4 chars, 2 edits for 5+ chars
        max_tolerance = 2 if len(norm_query) >= 5 else 1

        fuzzy_candidates: list[tuple[CompanyRecord, int, int]] = []
        for record in self.records:
            norm_name = self.normalize_text(record.name)
            name_words = [w for w in norm_name.split() if len(w) > 1]
            aliases = [self.normalize_text(a) for a in record.aliases]

            # Collect comparison targets: words, prefixes, ticker, aliases
            distances: list[int] = []

            for w in name_words:
                distances.append(self.levenshtein_distance(norm_query, w))
                if len(w) >= len(norm_query):
                    distances.append(self.levenshtein_distance(norm_query, w[: len(norm_query)]))

            for a in aliases:
                distances.append(self.levenshtein_distance(norm_query, a))
                if len(a) >= len(norm_query):
                    distances.append(self.levenshtein_distance(norm_query, a[: len(norm_query)]))

            if len(norm_query) >= 4:
                distances.append(self.levenshtein_distance(norm_query, record.ticker.lower()))

            min_d = min(distances) if distances else 99
            if min_d <= max_tolerance:
                # Secondary priority: word length difference
                diff_len = abs(len(norm_query) - len(record.name.split()[0]))
                fuzzy_candidates.append((record, min_d, diff_len))

        if fuzzy_candidates:
            # Deterministic sorting: lowest edit distance, then length difference, then ticker
            fuzzy_candidates.sort(key=lambda item: (item[1], item[2], item[0].ticker))
            top_fuzzy = [r.to_schema() for r, _, _ in fuzzy_candidates[:4]]
            return CompanySearchResponse(
                query=raw_query,
                results=top_fuzzy,
                fuzzy=True,
                ambiguous=len(top_fuzzy) > 1,
                count=len(top_fuzzy),
                match=top_fuzzy[0],
            )

        # ----------------------------------------------------
        # Stage 4: Dynamic Global Equity Search via Yahoo Finance
        # ----------------------------------------------------
        try:
            import urllib.request
            import urllib.parse
            import json

            encoded_q = urllib.parse.quote(raw_query)
            url = f"https://query2.finance.yahoo.com/v1/finance/search?q={encoded_q}&quotesCount=6&newsCount=0"
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            )
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                quotes = data.get("quotes", [])
                live_companies: list[Company] = []
                for q in quotes:
                    symbol = q.get("symbol")
                    name = q.get("shortname") or q.get("longname")
                    if not symbol or not name:
                        continue
                    if "=" in symbol and len(quotes) > 1:
                        continue
                    exchange = q.get("exchange", "GLOBAL")
                    market = "US"
                    if ".NS" in symbol or ".BO" in symbol:
                        market = "India"
                    elif ".TO" in symbol:
                        market = "Canada"
                    elif ".L" in symbol:
                        market = "UK"
                    elif ".DE" in symbol or ".PA" in symbol:
                        market = "Europe"

                    live_companies.append(
                        Company(
                            name=name,
                            ticker=symbol,
                            exchange=exchange,
                            market=market,
                            sector=q.get("sector") or q.get("industry") or "General",
                        )
                    )

                if live_companies:
                    return CompanySearchResponse(
                        query=raw_query,
                        results=live_companies[:5],
                        fuzzy=False,
                        ambiguous=len(live_companies) > 1,
                        count=len(live_companies),
                        match=live_companies[0],
                    )
        except Exception:
            pass

        # ----------------------------------------------------
        # Stage 5: No Result
        # ----------------------------------------------------
        return CompanySearchResponse(
            query=raw_query,
            results=[],
            fuzzy=False,
            ambiguous=False,
            count=0,
            match=None,
        )


# Singleton resolver instance
resolver = CompanyResolver()
