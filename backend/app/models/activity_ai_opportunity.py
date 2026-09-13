from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class ActivityAIOpportunity(Base):
    __tablename__ = "activity_ai_opportunities"

    activity_id: Mapped[int] = mapped_column(
        ForeignKey("activities.id"),
        primary_key=True,
    )

    ai_opportunity_id: Mapped[int] = mapped_column(
        ForeignKey("ai_opportunities.id"),
        primary_key=True,
    )

    impact_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    activity = relationship(
        "Activity",
    )

    ai_opportunity = relationship(
        "AIOpportunity",
        back_populates="activity_opportunities",
    )