from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class BetCreate(BaseModel):

    market_id: str
    outcome: str
    amount: int = Field(gt=0)


class BetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    wallet_id: int
    market_id: str
    outcome: str
    amount: int
    status: str
    entry_price: Decimal | None
    shares: Decimal | None
    created_at: datetime


class BetPage(BaseModel):
    items: list[BetRead]
    total: int
    limit: int
    offset: int