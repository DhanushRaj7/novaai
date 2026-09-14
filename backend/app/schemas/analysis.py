from pydantic import BaseModel, Field


class ActivityAnalysis(BaseModel):
    name: str
    description: str
    sequence: int = Field(ge=1)
    activity_type: str
    decision_required: bool


class AIOpportunityAnalysis(BaseModel):
    name: str
    description: str
    ai_capability: str

    automation_potential: float = Field(ge=0, le=1)
    human_involvement: float = Field(ge=0, le=1)
    expected_benefit: float = Field(ge=0, le=1)
    feasibility: float = Field(ge=0, le=1)
    strategic_alignment: float = Field(ge=0, le=1)
    risk_level: float = Field(ge=0, le=1)

    reasoning: str


class ProcessAnalysis(BaseModel):
    summary: str
    activities: list[ActivityAnalysis]
    ai_opportunities: list[AIOpportunityAnalysis]