from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.health import HealthResponse
from app.core.dependencies import get_db


router = APIRouter()



@router.get("/health", response_model=HealthResponse, description="Check Health status")
def health_check():
    return {"status": "healthy"}

@router.get("/health/db")
async def health_db_check(session: AsyncSession = Depends(get_db)):
    await session.execute(text("SELECT 1"))

    return {"status": "database connected"}




