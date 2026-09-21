from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.enterprise_intelligence import (
    get_enterprise_intelligence,
)

router = APIRouter(
    prefix="/intelligence",
    tags=["Enterprise Intelligence"],
)


@router.get("/enterprise")
def enterprise_intelligence(
    db: Session = Depends(get_db),
):
    return get_enterprise_intelligence(db)