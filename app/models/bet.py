from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, DateTime, func, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Bet(Base):
    __tablename__ = "bets"
    __table_args__ = (
        CheckConstraint("amount > 0", name="ck_bets_amount_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"), nullable=False)
    market_id: Mapped[str]
    outcome: Mapped[str]
    amount: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str]
    entry_price: Mapped[Decimal | None] = mapped_column(Numeric(precision=10, scale=8), nullable=True)
    shares: Mapped[Decimal | None] = mapped_column(Numeric(precision=20, scale=8), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
