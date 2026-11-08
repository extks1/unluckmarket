from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wallet import Wallet
from app.models.wallet_transaction import WalletTransaction


class WalletNotFoundError(Exception):
    pass


async def get_wallet_by_user_id(user_id: int, session: AsyncSession):
    statement = select(Wallet).where(Wallet.user_id == user_id)
    wallet = await session.scalar(statement)
    if wallet is None:
        raise WalletNotFoundError()
    return wallet

async def wallet_history(user_id: int, session: AsyncSession):
    wallet = await get_wallet_by_user_id(user_id, session)
    statement = select(WalletTransaction).where(WalletTransaction.wallet_id == wallet.id).order_by(WalletTransaction.id.desc())

    response = await session.scalars(statement)
    return response.all()

