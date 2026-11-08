from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from app.core.dependencies import get_db
from app.schemas.bet import BetRead, BetCreate, BetPage
from app.services.wallet_service import WalletNotFoundError
from app.services.bet_service import (
    place_bet,
    get_bets_by_user_id,
    get_bet_by_id,
    InsufficientFundsError,
    MarketNotFoundError,
    MarketNotActiveError,
    InvalidOutcomeError,
    InvalidMarketPriceError,
    BetNotFoundError,
)

router = APIRouter()


@router.post("/bets/{user_id}", response_model=BetRead, status_code=status.HTTP_201_CREATED)
async def create_bet(user_id: int, bet_data: BetCreate, session: AsyncSession = Depends(get_db)):
    try:
        user_bet = await place_bet(
            user_id=user_id,
            market_id=bet_data.market_id,
            outcome=bet_data.outcome,
            amount=bet_data.amount,
            session=session,
        )
        return user_bet

    except WalletNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )
    except InsufficientFundsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Insufficient funds"
        )
    except MarketNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Market not found"
        )
    except MarketNotActiveError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Market not active"
        )
    except InvalidOutcomeError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Invalid outcome"
        )
    except InvalidMarketPriceError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Market returned an invalid price"
        )


@router.get("/bets/{user_id}", response_model=BetPage)
async def get_user_bets(
        user_id: int,
        session: AsyncSession = Depends(get_db),
        status_filter: Literal["open"] | None = Query(default=None, alias="status"),
        limit: int = Query(default=50, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
        market_id: str | None = Query(default=None)
):
    try:
        response = await get_bets_by_user_id(
            user_id=user_id,
            session=session,
            status=status_filter,
            limit=limit,
            offset=offset,
            market_id=market_id
        )
        return response

    except WalletNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found"
        )

@router.get("/users/{user_id}/bets/{bet_id}", response_model=BetRead)
async def get_user_bet(user_id: int, bet_id: int, session: AsyncSession = Depends(get_db)):
    try:
        return await get_bet_by_id(user_id, bet_id, session)

    except BetNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bet not found"
        )
    except WalletNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found",
        )