from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.ai_opportunity import AIOpportunity
from app.models.initiative import TransformationInitiative
from app.models.ai_opportunity_initiative import AIOpportunityInitiative

router = APIRouter(
    prefix="/initiative-links",
    tags=["Initiative Links"],
)


class InitiativeLinkCreate(BaseModel):
    ai_opportunity_id: int
    initiative_id: int
    relationship_type: str = "supports"


@router.post("")
def create_initiative_link(
    link_data: InitiativeLinkCreate,
    db: Session = Depends(get_db),
):
    opportunity = db.get(
        AIOpportunity,
        link_data.ai_opportunity_id,
    )

    if opportunity is None:
        raise HTTPException(
            status_code=404,
            detail="AI opportunity not found",
        )

    initiative = db.get(
        TransformationInitiative,
        link_data.initiative_id,
    )

    if initiative is None:
        raise HTTPException(
            status_code=404,
            detail="Transformation initiative not found",
        )

    existing = db.get(
        AIOpportunityInitiative,
        (
            link_data.ai_opportunity_id,
            link_data.initiative_id,
        ),
    )

    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail="Relationship already exists",
        )

    link = AIOpportunityInitiative(
        ai_opportunity_id=link_data.ai_opportunity_id,
        initiative_id=link_data.initiative_id,
        relationship_type=link_data.relationship_type,
    )

    db.add(link)
    db.commit()

    return {
        "ai_opportunity_id": link.ai_opportunity_id,
        "initiative_id": link.initiative_id,
        "relationship_type": link.relationship_type,
    }