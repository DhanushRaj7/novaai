from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class ResearchSource(Base):
    __tablename__ = "research_sources"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    publisher: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    source_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    publication_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    retrieved_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    evidence = relationship(
        "Evidence",
        back_populates="source",
        cascade="all, delete-orphan",
    )

    chunks = relationship(
    "ResearchChunk",
    back_populates="source",
    cascade="all, delete-orphan",
    )