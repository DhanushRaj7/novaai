from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Role(Base):
    __tablename__ = "roles"

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

    organisation = relationship(
        "Organisation",
    )

    process_roles = relationship(
        "ProcessRole",
        back_populates="role",
        cascade="all, delete-orphan",
    )

    role_skills = relationship(
        "RoleSkill",
        back_populates="role",
        cascade="all, delete-orphan",
    )