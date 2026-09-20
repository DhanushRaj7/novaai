from pydantic import BaseModel, Field


class EvidenceAnalysis(BaseModel):
    claim: str
    supporting_excerpt: str
    relevance_score: float = Field(ge=0, le=1)
    confidence_score: float = Field(ge=0, le=1)