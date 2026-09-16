from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(primary_key=True)

    source_id: Mapped[int] = mapped_column(
        ForeignKey("research_sources.id"),
        nullable=False,
    )

    ai_opportunity_id: Mapped[int] = mapped_column(
        ForeignKey("ai_opportunities.id"),
        nullable=False,
    )

    claim: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    excerpt: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    relevance_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    confidence_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    source = relationship(
        "ResearchSource",
        back_populates="evidence",
    )

    ai_opportunity = relationship(
        "AIOpportunity",
    )