from fastapi import APIRouter, HTTPException, status

from app.schemas.market import Market
from app.services.market_service import list_markets, get_market_by_id

router = APIRouter()



@router.get("/markets/",response_model=list[Market], description="Get markets info")
async def get_markets(active: bool | None = None):
    markets = await list_markets(active)
    return markets

@router.get("/markets/{market_id}",response_model=Market, description="Get markets info")
async def get_markets_by_id(market_id: str) -> Market:
    market = await get_market_by_id(market_id)
    if market is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="market_id not found")
    return market