import uuid
from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, String, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models.review import Review


class Film(Base):
    __tablename__ = "films"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    title: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    release_year: Mapped[int] = mapped_column(nullable=False)
    genre: Mapped[str] = mapped_column(String(50), default="Drama", nullable=False)
    director: Mapped[str] = mapped_column(String(100), default="Unknown", nullable=False)
    hero: Mapped[str] = mapped_column(String(100), server_default="Unknown", default="Unknown", nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, server_default="false", default=False, nullable=False)



    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationship to reviews
    reviews: Mapped[List["Review"]] = relationship(
        back_populates="film",
        cascade="all, delete-orphan",
    )
