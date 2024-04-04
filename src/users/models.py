from datetime import datetime
from uuid import uuid4, UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(length=128), index=True, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(length=64), index=True, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(length=512))
    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    created_at: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow)
