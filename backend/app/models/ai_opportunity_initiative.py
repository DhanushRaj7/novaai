from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class AIOpportunityInitiative(Base):
    __tablename__ = "ai_opportunity_initiatives"

    ai_opportunity_id: Mapped[int] = mapped_column(
        ForeignKey("ai_opportunities.id"),
        primary_key=True,
    )

    initiative_id: Mapped[int] = mapped_column(
        ForeignKey("transformation_initiatives.id"),
        primary_key=True,
    )

    relationship_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    ai_opportunity = relationship(
        "AIOpportunity",
        back_populates="initiative_links",
    )

    initiative = relationship(
        "TransformationInitiative",
        back_populates="opportunity_links",
    )