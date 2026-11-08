from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)

    __tablename__ = "users"
