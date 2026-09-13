from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class RoleSkill(Base):
    __tablename__ = "role_skills"

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        primary_key=True,
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id"),
        primary_key=True,
    )

    importance: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    skill_status: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    role = relationship(
        "Role",
        back_populates="role_skills",
    )

    skill = relationship(
        "Skill",
        back_populates="role_skills",
    )