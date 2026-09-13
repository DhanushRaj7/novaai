from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class InitiativeDependency(Base):
    __tablename__ = "initiative_dependencies"

    initiative_id: Mapped[int] = mapped_column(
        ForeignKey("transformation_initiatives.id"),
        primary_key=True,
    )

    depends_on_initiative_id: Mapped[int] = mapped_column(
        ForeignKey("transformation_initiatives.id"),
        primary_key=True,
    )

    dependency_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    initiative = relationship(
        "TransformationInitiative",
        foreign_keys=[initiative_id],
    )

    depends_on_initiative = relationship(
        "TransformationInitiative",
        foreign_keys=[depends_on_initiative_id],
    )