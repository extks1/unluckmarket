from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.markets import router as markets_router
from app.api.routes.users import router as users_router
from app.api.routes.wallets import router as wallets_router
from app.api.routes.bets import router as bets_router


app = FastAPI()
app.include_router(health_router)
app.include_router(markets_router)
app.include_router(users_router)
app.include_router(wallets_router)
app.include_router(bets_router)

