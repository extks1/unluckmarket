from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.models.user import User
from app.models.wallet import Wallet
from app.schemas.user import UserCreate
from app.models.wallet_transaction import WalletTransaction


class UserAlreadyExistsError(Exception):
    pass

class UserNotFoundError(Exception):
    pass


async def create_user(user_create: UserCreate, session: AsyncSession) -> User:
    try:
        user = User(telegram_id=user_create.telegram_id)
        session.add(user)

        await session.flush()
        wallet = Wallet(user_id=user.id, balance=1000)
        session.add(wallet)

        await session.flush()
        wallet_transaction = WalletTransaction(
            wallet_id=wallet.id, amount=1000, reason="initial_credit", balance_after=1000
        )
        session.add(wallet_transaction)

        await session.commit()
    except IntegrityError as error:
        await session.rollback()
        raise UserAlreadyExistsError from error
    await session.refresh(user)
    return user

async def get_user_by_telegram_id(telegram_id: int, session: AsyncSession) -> User:
    statement = select(User).where(User.telegram_id == telegram_id)
    user = await session.scalar(statement)
    if user is None:
        raise UserNotFoundError()
    return user




