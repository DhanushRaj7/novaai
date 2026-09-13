from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)

    process_id: Mapped[int] = mapped_column(
        ForeignKey("processes.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    sequence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    activity_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    decision_required: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    process = relationship(
        "Process",
        back_populates="activities",
    )