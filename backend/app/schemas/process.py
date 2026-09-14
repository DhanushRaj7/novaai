from pydantic import BaseModel, ConfigDict


class ProcessCreate(BaseModel):
    value_chain_stage_id: int
    name: str
    description: str
    business_purpose: str | None = None
    current_challenges: str | None = None


class ProcessResponse(BaseModel):
    id: int
    value_chain_stage_id: int
    name: str
    description: str
    business_purpose: str | None
    current_challenges: str | None
    status: str
    priority_score: float | None

    model_config = ConfigDict(from_attributes=True)