from typing import Optional
from pydantic import BaseModel, Field


class Company(BaseModel):
    name: str = Field(..., description="Full legal name of the company")
    ticker: str = Field(..., description="Stock symbol/ticker")
    exchange: str = Field(..., description="Exchange name e.g. NASDAQ, NYSE")
    market: str = Field(..., description="Country or region market e.g. US")
    sector: Optional[str] = Field(default=None, description="Business sector e.g. Technology")


class CompanySearchResponse(BaseModel):
    query: str = Field(..., description="Search query string")
    results: list[Company] = Field(default_factory=list, description="Matched companies")
    fuzzy: bool = Field(default=False, description="Whether fuzzy matching was triggered")
    ambiguous: bool = Field(default=False, description="Whether multiple candidate companies matched")
    count: int = Field(default=0, description="Number of results found")
    match: Optional[Company] = Field(default=None, description="Primary normalized company match")
