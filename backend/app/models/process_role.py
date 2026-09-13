from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class ProcessRole(Base):
    __tablename__ = "process_roles"

    process_id: Mapped[int] = mapped_column(
        ForeignKey("processes.id"),
        primary_key=True,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        primary_key=True,
    )

    responsibility: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    process = relationship(
        "Process",
    )

    role = relationship(
        "Role",
        back_populates="process_roles",
    )