from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class ValueChainStage(Base):
    __tablename__ = "value_chain_stages"

    id: Mapped[int] = mapped_column(primary_key=True)

    organisation_id: Mapped[int] = mapped_column(
        ForeignKey("organisations.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)

    organisation = relationship(
        "Organisation",
        back_populates="value_chain_stages",
    )

    processes = relationship(
        "Process",
        back_populates="value_chain_stage",
        cascade="all, delete-orphan",
    )