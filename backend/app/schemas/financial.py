from typing import Optional
from pydantic import BaseModel, Field


class PriceQuote(BaseModel):
    current_price: Optional[float] = Field(default=None, description="Current or latest close price")
    previous_close: Optional[float] = Field(default=None, description="Previous day close price")
    price_change: Optional[float] = Field(default=None, description="Absolute price change")
    price_change_percent: Optional[float] = Field(default=None, description="Percentage price change")
    currency: str = Field(default="USD", description="Currency code")
    formatted_price: str = Field(default="N/A", description="Formatted price string e.g. $228.40")
    formatted_change: str = Field(default="N/A", description="Formatted change string e.g. +2.41%")
    change_direction: str = Field(default="up", description="'up' | 'down' | 'neutral'")


class FundamentalMetrics(BaseModel):
    market_cap: Optional[float] = Field(default=None, description="Market capitalization in base currency")
    formatted_market_cap: str = Field(default="N/A", description="Formatted market cap e.g. $3.5T")
    revenue: Optional[float] = Field(default=None, description="Total trailing twelve months revenue")
    formatted_revenue: str = Field(default="N/A", description="Formatted revenue e.g. $112.0B")
    net_income: Optional[float] = Field(default=None, description="Net income / profit")
    formatted_net_income: str = Field(default="N/A", description="Formatted net income e.g. $26.4B")
    eps: Optional[float] = Field(default=None, description="Diluted earnings per share")
    formatted_eps: str = Field(default="N/A", description="Formatted EPS e.g. $7.32")
    pe_ratio: Optional[float] = Field(default=None, description="Price to Earnings multiple")
    formatted_pe: str = Field(default="N/A", description="Formatted P/E e.g. 31.2")
    operating_margin: Optional[float] = Field(default=None, description="Operating margin decimal e.g. 0.299")
    formatted_operating_margin: str = Field(default="N/A", description="Formatted operating margin e.g. 29.9%")
    net_margin: Optional[float] = Field(default=None, description="Net profit margin decimal e.g. 0.236")
    formatted_net_margin: str = Field(default="N/A", description="Formatted net margin e.g. 23.6%")
    revenue_growth: Optional[float] = Field(default=None, description="YoY revenue growth decimal e.g. 0.12")
    formatted_revenue_growth: str = Field(default="N/A", description="Formatted revenue growth e.g. +12.0%")


class SnapshotMetric(BaseModel):
    label: str = Field(..., description="Metric label")
    value: str = Field(..., description="Formatted metric value")


class RevenueYearItem(BaseModel):
    year: int = Field(..., description="Fiscal year")
    amount: float = Field(..., description="Revenue amount in Billions")
    formatted_amount: str = Field(default="$0B", description="Formatted revenue string")


class FinancialData(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")
    quote: PriceQuote = Field(..., description="Price and change information")
    fundamentals: FundamentalMetrics = Field(..., description="Key fundamental ratios and figures")
    snapshot: list[SnapshotMetric] = Field(default_factory=list, description="Ordered metric snapshot for UI cards")
    revenue_history: list[RevenueYearItem] = Field(default_factory=list, description="Annual revenue timeline")
    price_points: list[float] = Field(default_factory=list, description="Historical price series for chart")
    historical_dates: list[str] = Field(default_factory=list, description="Historical dates/months for chart labels")
    is_live: bool = Field(default=True, description="True if retrieved from live market data layer")
    error_message: Optional[str] = Field(default=None, description="Error or fallback reason if live fetch failed")
