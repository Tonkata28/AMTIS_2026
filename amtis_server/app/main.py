from fastapi import FastAPI, Request
from app.routers import team, users, stocks, sessions, wallet, reports, forex, regulations
from .errors.exception_handlers import register_exception_handlers
from .adapters.market import market
from .db.store import db

app = FastAPI()

app.include_router(team.router)
app.include_router(users.router)
app.include_router(stocks.router)
app.include_router(sessions.router)
app.include_router(wallet.router)
app.include_router(reports.router)
app.include_router(forex.router)
app.include_router(regulations.router)
market.authenticate_session()
db["regulations"] = market.get_market_regulations()["regulations"]

register_exception_handlers(app=app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)