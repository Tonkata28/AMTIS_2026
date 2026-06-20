from fastapi import FastAPI
from .routers import team, users, stocks, sessions, wallet, reports, forex, regulations
from .errors.exception_handlers import register_exception_handlers
from .adapters.market import market
from .db.store import db

from contextlib import asynccontextmanager
import asyncio
from .errors.error_codes import Codes
from .errors.exceptions import AppError


async def refresh_regulations():
    while True:
        try:
            db["regulations"] = market.get_market_regulations()
        
        except Exception as e:
            print(f"Regulation refresh failed: {e}")
            raise AppError(Codes.MARKED_CLOSED)

        await asyncio.sleep(3600) # refreshes every hour

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        market.authenticate_session()
    except Exception:
        raise AppError(Codes.MARKED_CLOSED)

    task = asyncio.create_task(refresh_regulations())

    yield

    task.cancel()


app = FastAPI(lifespan=lifespan)

app.include_router(team.router)
app.include_router(users.router)
app.include_router(stocks.router)
app.include_router(sessions.router)
app.include_router(wallet.router)
app.include_router(reports.router)
app.include_router(forex.router)
app.include_router(regulations.router)
register_exception_handlers(app=app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)