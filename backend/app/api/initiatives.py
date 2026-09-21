from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.initiative import TransformationInitiative

router = APIRouter(
    prefix="/initiatives",
    tags=["Transformation Initiatives"],
)


class InitiativeCreate(BaseModel):
    organisation_id: int
    name: str
    description: str | None = None
    status: str = "planned"
    priority: float | None = None
    expected_benefit: str | None = None


class InitiativeResponse(BaseModel):
    id: int
    organisation_id: int
    name: str
    description: str | None
    status: str
    priority: float | None
    expected_benefit: str | None

    class Config:
        from_attributes = True


@router.post("", response_model=InitiativeResponse)
def create_initiative(
    initiative_data: InitiativeCreate,
    db: Session = Depends(get_db),
):
    initiative = TransformationInitiative(
        organisation_id=initiative_data.organisation_id,
        name=initiative_data.name,
        description=initiative_data.description,
        status=initiative_data.status,
        priority=initiative_data.priority,
        expected_benefit=initiative_data.expected_benefit,
    )

    db.add(initiative)
    db.commit()
    db.refresh(initiative)

    return initiative


@router.get("", response_model=list[InitiativeResponse])
def get_initiatives(
    db: Session = Depends(get_db),
):
    result = db.execute(
        select(TransformationInitiative)
        .order_by(TransformationInitiative.priority.desc())
    )

    return result.scalars().all()


@router.get("/{initiative_id}", response_model=InitiativeResponse)
def get_initiative(
    initiative_id: int,
    db: Session = Depends(get_db),
):
    initiative = db.get(
        TransformationInitiative,
        initiative_id,
    )

    if initiative is None:
        raise HTTPException(
            status_code=404,
            detail="Transformation initiative not found",
        )

    return initiative