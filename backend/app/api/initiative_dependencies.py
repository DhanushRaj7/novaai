from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.initiative import TransformationInitiative
from app.models.initiative_dependency import InitiativeDependency

router = APIRouter(
    prefix="/initiative-dependencies",
    tags=["Initiative Dependencies"],
)


class DependencyCreate(BaseModel):
    initiative_id: int
    depends_on_initiative_id: int
    dependency_type: str | None = None
    description: str | None = None


@router.post("")
def create_dependency(
    dependency_data: DependencyCreate,
    db: Session = Depends(get_db),
):
    initiative = db.get(
        TransformationInitiative,
        dependency_data.initiative_id,
    )

    if initiative is None:
        raise HTTPException(
            status_code=404,
            detail="Initiative not found",
        )

    depends_on = db.get(
        TransformationInitiative,
        dependency_data.depends_on_initiative_id,
    )

    if depends_on is None:
        raise HTTPException(
            status_code=404,
            detail="Dependency initiative not found",
        )

    if (
        dependency_data.initiative_id
        == dependency_data.depends_on_initiative_id
    ):
        raise HTTPException(
            status_code=400,
            detail="An initiative cannot depend on itself",
        )

    existing = db.get(
        InitiativeDependency,
        (
            dependency_data.initiative_id,
            dependency_data.depends_on_initiative_id,
        ),
    )

    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail="Dependency already exists",
        )

    dependency = InitiativeDependency(
        initiative_id=dependency_data.initiative_id,
        depends_on_initiative_id=dependency_data.depends_on_initiative_id,
        dependency_type=dependency_data.dependency_type,
        description=dependency_data.description,
    )

    db.add(dependency)
    db.commit()

    return {
        "initiative_id": dependency.initiative_id,
        "depends_on_initiative_id": dependency.depends_on_initiative_id,
        "dependency_type": dependency.dependency_type,
        "description": dependency.description,
    }


@router.get("")
def get_dependencies(
    db: Session = Depends(get_db),
):
    dependencies = (
        db.query(InitiativeDependency)
        .order_by(
            InitiativeDependency.initiative_id,
            InitiativeDependency.depends_on_initiative_id,
        )
        .all()
    )

    return [
        {
            "initiative_id": item.initiative_id,
            "depends_on_initiative_id": item.depends_on_initiative_id,
            "dependency_type": item.dependency_type,
            "description": item.description,
        }
        for item in dependencies
    ]