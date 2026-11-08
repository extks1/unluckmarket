from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.schemas.wallet import WalletRead
from app.schemas.wallet_transaction import WalletTransactionRead
from app.services.wallet_service import get_wallet_by_user_id, WalletNotFoundError, wallet_history

router = APIRouter()


@router.get("/wallets/{user_id}", response_model=WalletRead)
async def get_wallet_id(user_id: int, session: AsyncSession = Depends(get_db)):
    try:
        return await get_wallet_by_user_id(user_id, session)
    except WalletNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")


@router.get("/wallets/{user_id}/transactions", response_model=list[WalletTransactionRead])
async def get_wallet_transactions(user_id: int, session: AsyncSession = Depends(get_db)):
    try:
        return await wallet_history(user_id, session)
    except WalletNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")
