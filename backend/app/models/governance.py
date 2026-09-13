from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class GovernanceAssessment(Base):
    __tablename__ = "governance_assessments"

    id: Mapped[int] = mapped_column(primary_key=True)

    ai_opportunity_id: Mapped[int] = mapped_column(
        ForeignKey("ai_opportunities.id"),
        nullable=False,
        unique=True,
    )

    data_risk: Mapped[float | None] = mapped_column(Float, nullable=True)
    privacy_risk: Mapped[float | None] = mapped_column(Float, nullable=True)
    bias_risk: Mapped[float | None] = mapped_column(Float, nullable=True)

    oversight_requirement: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    explainability_requirement: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    security_risk: Mapped[float | None] = mapped_column(Float, nullable=True)
    decision_impact: Mapped[float | None] = mapped_column(Float, nullable=True)
    regulatory_exposure: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    model_risk: Mapped[float | None] = mapped_column(Float, nullable=True)
    monitoring_requirement: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    overall_risk: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    reasoning: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    ai_opportunity = relationship(
        "AIOpportunity",
    )