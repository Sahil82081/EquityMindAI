from pydantic import BaseModel, Field


class DebatePoint(BaseModel):
    """Individual debate argument backed by auditable evidence."""

    title: str = Field(..., description="Short, punchy title of the argument")
    description: str = Field(..., description="Detailed argument explanation citing specific metrics or facts")
    source: str = Field(..., description="Specific citation source e.g. SEC 10-K, Income Statement, Verified News Wire")


class DebateSide(BaseModel):
    """Structured debate case presented by Bull or Bear Agent."""

    confidence: int = Field(..., ge=0, le=100, description="Agent confidence score out of 100")
    arguments: list[DebatePoint] = Field(default_factory=list, description="3-4 evidence-backed structured arguments")
    key_metrics: str = Field(..., description="Summary string of core metrics supporting this side")


class JudgeAdjudicationOutput(BaseModel):
    """Pydantic validated structured output from the Judge Agent."""

    bull_strengths: list[str] = Field(..., description="Strongest verified points in the bull thesis")
    bull_weaknesses: list[str] = Field(..., description="Identified flaws or unverified assumptions in the bull thesis")
    bear_strengths: list[str] = Field(..., description="Strongest verified points in the bear thesis")
    bear_weaknesses: list[str] = Field(..., description="Flaws or exaggerated concerns in the bear thesis")
    evidence_comparison: str = Field(..., description="Objective comparison of which arguments have stronger empirical support")
    balanced_conclusion: str = Field(
        ...,
        description="Comprehensive, balanced adjudication weighing both sides without simply picking a one-sided winner",
    )


class DebateResult(BaseModel):
    """Final adjudicated Bull vs Bear debate outcome."""

    bull: DebateSide = Field(..., description="Bull case arguments and metrics")
    bear: DebateSide = Field(..., description="Bear case arguments and metrics")
    judge_conclusion: str = Field(..., description="Adjudicated balanced conclusion produced by Judge Agent")
    adjudication_detail: JudgeAdjudicationOutput = Field(
        default_factory=lambda: JudgeAdjudicationOutput(
            bull_strengths=[],
            bull_weaknesses=[],
            bear_strengths=[],
            bear_weaknesses=[],
            evidence_comparison="",
            balanced_conclusion="",
        ),
        description="Detailed structured breakdown from the Judge Agent",
    )
