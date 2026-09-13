from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Process(Base):
    __tablename__ = "processes"

    id: Mapped[int] = mapped_column(primary_key=True)

    value_chain_stage_id: Mapped[int] = mapped_column(
        ForeignKey("value_chain_stages.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    business_purpose: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    current_challenges: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="active",
        nullable=False,
    )
    priority_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    value_chain_stage = relationship(
        "ValueChainStage",
        back_populates="processes",
    )

    activities = relationship(
    "Activity",
    back_populates="process",
    cascade="all, delete-orphan",
    )

    process_roles = relationship(
    "ProcessRole",
    back_populates="process",
    cascade="all, delete-orphan",
    )