from datetime import datetime

from sqlalchemy import DateTime, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class AIOpportunity(Base):
    __tablename__ = "ai_opportunities"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    ai_capability: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    automation_potential: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    human_involvement: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    expected_benefit: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    feasibility: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    strategic_alignment: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    risk_level: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    priority_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    reasoning: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    activity_opportunities = relationship(
        "ActivityAIOpportunity",
        back_populates="ai_opportunity",
        cascade="all, delete-orphan",
    )

    evidence = relationship(
    "Evidence",
    back_populates="ai_opportunity",
    cascade="all, delete-orphan",
    )


    initiative_links = relationship(
    "AIOpportunityInitiative",
    back_populates="ai_opportunity",
    cascade="all, delete-orphan",
    )