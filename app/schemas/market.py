from pydantic import BaseModel

class Market(BaseModel):
    id: str
    question: str
    active: bool
    description: str
    outcomes: str