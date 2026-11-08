from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import create_user
from app.services.user_service import UserAlreadyExistsError, UserNotFoundError
from app.services.user_service import get_user_by_telegram_id


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(user_data: UserCreate, session: AsyncSession = Depends(get_db)):
    try:
        return await create_user(user_create=user_data, session=session)
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="user with this telegram_id already exists"
        )

@router.get("/{telegram_id}", response_model=UserRead)
async def get_user_by_id(telegram_id: int, session: AsyncSession = Depends(get_db)):
     try:
         return await get_user_by_telegram_id(telegram_id, session)
     except UserNotFoundError:
         raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="user Not Found"
         )
