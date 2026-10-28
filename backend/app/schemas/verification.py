from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field


class VerificationStatus(str, Enum):
    """Rigorous factual verification classification for research claims."""

    VERIFIED = "Verified"
    PARTIALLY_VERIFIED = "Partially Verified"
    UNSUPPORTED = "Unsupported"


class Evidence(BaseModel):
    """Structured evidence retrieved from ground-truth filings and deterministic calculations."""

    source_data: str = Field(
        ...,
        description="Source numbers retrieved from verified data (e.g. Previous revenue $383.3B · Current revenue $391.0B)",
    )
    calculation: str = Field(
        ...,
        description="Mathematical calculation executed in Python (e.g. (391.0 - 383.3) / 383.3 * 100 = +2.0%)",
    )
    retrieved_values: dict[str, Any] = Field(
        default_factory=dict,
        description="Raw key-value pairs extracted from source financial data or news",
    )
    formula: Optional[str] = Field(
        default=None,
        description="Formula description or audit equation",
    )


class VerificationResult(BaseModel):
    """Adjudicated verification outcome comparing the claim statement against Python calculations."""

    status: VerificationStatus = Field(
        ...,
        description="Verification outcome: Verified, Partially Verified, or Unsupported",
    )
    status_code: str = Field(
        default="ok",
        description="UI compatible status code: ok (Verified), warn (Partially Verified), bad (Unsupported)",
    )
    result_text: str = Field(
        ...,
        description="Audited outcome text explaining calculation match or lack of evidence",
    )
    confidence_score: int = Field(
        default=95,
        ge=0,
        le=100,
        description="Algorithmic confidence in verification result (0-100)",
    )
    discrepancy_explanation: Optional[str] = Field(
        default=None,
        description="Explanation of any variance, benchmark discrepancy, or missing guidance figures",
    )


class ClaimProof(BaseModel):
    """Individual proof step maintaining direct compatibility with the existing Claims UI."""

    label: str = Field(..., description="Step label e.g. 'Source data', 'Calculation'")
    detail: str = Field(..., description="Auditable data details or mathematical formula")


class Claim(BaseModel):
    """Fact-checked empirical claim grounded in audited source data."""

    id: Optional[str] = Field(default=None, description="Unique claim identifier e.g. c1, c2")
    statement: str = Field(..., description="Verifiable factual claim statement")
    status: str = Field(
        ...,
        description="Verification status string: 'Verified', 'Partially Verified', 'Unsupported' or 'ok', 'warn', 'bad'",
    )
    verification_status: VerificationStatus = Field(
        default=VerificationStatus.VERIFIED,
        description="Strongly typed verification status",
    )
    evidence: Evidence = Field(..., description="Structured ground-truth evidence and math")
    verification_result: VerificationResult = Field(
        ..., description="Verification audit outcome"
    )
    proofs: list[ClaimProof] = Field(
        default_factory=list,
        description="Ordered proof chain displayed in the Claims UI",
    )
    result: str = Field(..., description="Final verification result text")
