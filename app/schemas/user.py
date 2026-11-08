from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    telegram_id: int = Field(gt=0)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int 
    telegram_id: int