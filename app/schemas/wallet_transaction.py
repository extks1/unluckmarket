from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WalletTransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    wallet_id: int
    amount: int
    reason: str
    balance_after: int
    created_at: datetime
