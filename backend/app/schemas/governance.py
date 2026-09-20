from pydantic import BaseModel, Field


class GovernanceAnalysis(BaseModel):
    data_risk: float = Field(ge=0, le=1)
    privacy_risk: float = Field(ge=0, le=1)
    bias_risk: float = Field(ge=0, le=1)

    oversight_requirement: str
    explainability_requirement: str

    security_risk: float = Field(ge=0, le=1)
    decision_impact: float = Field(ge=0, le=1)
    regulatory_exposure: float = Field(ge=0, le=1)
    model_risk: float = Field(ge=0, le=1)

    monitoring_requirement: str

    reasoning: str