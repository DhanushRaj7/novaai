from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class TransformationInitiative(Base):
    __tablename__ = "transformation_initiatives"

    id: Mapped[int] = mapped_column(primary_key=True)

    organisation_id: Mapped[int] = mapped_column(
        ForeignKey("organisations.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="planned",
        nullable=False,
    )

    priority: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    expected_benefit: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    organisation = relationship("Organisation")

    opportunity_links = relationship(
    "AIOpportunityInitiative",
    back_populates="initiative",
    cascade="all, delete-orphan",
    )