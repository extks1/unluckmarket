import json

from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bet import Bet
from app.models.wallet_transaction import WalletTransaction
from app.services.market_service import get_market_by_id
from app.services.wallet_service import get_wallet_by_user_id


class InsufficientFundsError(Exception):
    pass

class MarketNotFoundError(Exception):
    pass

class MarketNotActiveError(Exception):
    pass

class InvalidOutcomeError(Exception):
    pass

class InvalidMarketPriceError(Exception):
    pass

class BetNotFoundError(Exception):
    pass


async def place_bet(user_id: int, market_id: str, outcome: str, amount: int, session: AsyncSession) -> Bet:
    is_market = await get_market_by_id(market_id)
    if is_market is None:
        raise MarketNotFoundError()
    elif is_market["active"] is False:
        raise MarketNotActiveError()

    available_outcomes = json.loads(is_market["outcomes"])
    if outcome not in available_outcomes:
        raise InvalidOutcomeError()

    outcome_prices = json.loads(is_market["outcomePrices"])
    outcome_index = available_outcomes.index(outcome)
    entry_price = Decimal(outcome_prices[outcome_index])
    wallet = await get_wallet_by_user_id(user_id, session)


    if entry_price <= 0:
        raise InvalidMarketPriceError()
    shares = amount / entry_price


    if wallet.balance < amount:
        raise InsufficientFundsError()
    wallet.balance -= amount
    bet = Bet(wallet_id = wallet.id, market_id = market_id, outcome=outcome, amount=amount, status="open", entry_price=entry_price, shares=shares)
    transaction = WalletTransaction(wallet_id=wallet.id, amount=-amount, reason="bet_placed", balance_after=wallet.balance)

    session.add(bet)
    session.add(transaction)

    await session.commit()
    await session.refresh(bet)
    return bet


async def get_bets_by_user_id(
        user_id: int,
        session: AsyncSession,
        status: str | None = None,
        limit: int = 50,
        offset: int = 0,
        market_id: str | None = None
):
    wallet = await get_wallet_by_user_id(user_id, session)
    filters = [Bet.wallet_id == wallet.id]
    if status is not None:
        filters.append(Bet.status == status)
    if market_id is not None:
        filters.append(Bet.market_id == market_id)

    count_statement = select(func.count(Bet.id)).where(*filters)
    total = await session.scalar(count_statement)
    statement = (select(Bet).where(*filters).order_by(Bet.id.desc()).limit(limit).offset(offset))
    result = await session.scalars(statement)
    items = result.all()
    return {
        "items": items,
        "total": total or 0,
        "limit": limit,
        "offset": offset,
    }


async def get_bet_by_id(user_id: int, bet_id: int, session: AsyncSession):
    wallet = await get_wallet_by_user_id(user_id, session)
    statement = select(Bet).where(Bet.wallet_id == wallet.id, Bet.id == bet_id)
    bet = await session.scalar(statement)
    if bet is None:
        raise BetNotFoundError()
    return bet