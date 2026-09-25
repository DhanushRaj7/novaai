from pydantic import BaseModel, ConfigDict
from pydantic import BaseModel, Field


class NewProcessAnalysisRequest(BaseModel):
    name: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=10, max_length=2000)
    value_chain_stage_id: int



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