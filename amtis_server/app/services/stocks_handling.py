from fastapi.responses import JSONResponse
from ..models.stocks import StocksFilter, BuyStockRequest, SellStockRequest, BuyStocksResult, SellStocksResult, BuyStockMaxPriceRequest, BuyStockMultiCurrencyResult, SellStockMultiCurrencyResult, SellStockMinPriceRequest
from ..models.user import StoredUser
from ..enums.http import AcceptStocksFormats
from ..utils.serialization import to_html, to_csv
from ..adapters.market import market
from ..errors.error_codes import Codes
from ..errors.exceptions import AppError, ERRORS
from ..models.user import UserStock
from ..db.store import db
from decimal import Decimal
from ..services.transactions_handling import withdraw_money, deposit_money
from datetime import datetime, timezone
from ..services.users_handling import check_user_exists


def format_stocks(stocks: list[dict], fmt: str | None, fields: list[str]):
    
    if fmt == AcceptStocksFormats.CSV:
        return to_csv(stocks, fields)

    if fmt == AcceptStocksFormats.HTML:
        return to_html(stocks, fields)


    # application/json format, */* and no value for Accept header fall in this case -> returning json format
    return stocks


def filter_stocks(fp: StocksFilter, stocks: list):

    if fp.ticker is not None:
        stocks = [r for r in stocks if r["ticker"] == fp.ticker]

    if fp.countryCode is not None:
        stocks = [r for r in stocks if r["countryCode"] == fp.countryCode]
    
    if fp.minBuyPrice is not None:
        stocks = [r for r in stocks if r["buyPrice"] >= fp.minBuyPrice]

    if fp.maxBuyPrice is not None:
        stocks = [r for r in stocks if r["buyPrice"] <= fp.maxBuyPrice]

    if fp.minSellPrice is not None:
        stocks = [r for r in stocks if r["sellPrice"] >= fp.minSellPrice]

    if fp.maxSellPrice is not None:
        stocks = [r for r in stocks if r["sellPrice"] <= fp.maxSellPrice]
     
    if fp.sortBy is not None:
        descending = fp.sortOrder == "desc"
        stocks = sorted(stocks, key = lambda x: x[fp.sortBy], reverse=descending)
    

    return stocks


def merge_stocks_prices(stocks: list[dict], prices: list[dict]) -> list[dict]:
    
    result = []

    for p in prices:

        for s in stocks:
            if s["ticker"] == p["ticker"]:
                result.append(
                {
                    "ticker": s["ticker"],
                    "name": s["name"],
                    "countryCode": s["countryOfOrigin"],
                    "currency": s["currency"],
                    "buyPrice": p["buy"],
                    "sellPrice": p["sell"]
                }
                )

    return result


def check_stocks_exists(ticker) -> dict:
    
    stocks = market.get_stocks_prices()
    current_stock_specs = next((s for s in stocks if s["ticker"] == ticker), None)
    
    if current_stock_specs is None:
        raise AppError(Codes.NOT_FOUND)

    return current_stock_specs


def check_stocks_exists_multi_curr(ticker) -> dict:
    
    stocks = market.get_stocks_v2()
    stocks_prices = market.get_prices_v2()

    current_stock_details = next((s for s in stocks if s["ticker"] == ticker), None)
    current_stock_prices = next((s for s in stocks_prices if s["ticker"] == ticker), None)
    
    if current_stock_details is None or current_stock_prices is None:
        raise AppError(Codes.NOT_FOUND)


    return {
        "buyPrice": current_stock_prices["buy"],
        "sellPrice": current_stock_prices["sell"],
        "countryCode": current_stock_details["countryOfOrigin"],
        "currency": current_stock_details["currency"],
        "name": current_stock_details["name"]
    }


def _record_transaction(type: str, ticker: str, countryCode: str, quantity: int, price: Decimal, currency: str, user_id: str):

    db["users"][user_id].transactions.append({
        "type": type,
        "ticker": ticker,
        "countryCode": countryCode,
        "quantity": quantity,
        "price": price,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "currency": currency
    })


def handle_buy_stock_request(buy_request: BuyStockRequest, user_id: str) -> BuyStocksResult:
    current_stock_specs = check_stocks_exists(ticker=buy_request.ticker)

    withdraw_money(user_id, Decimal(buy_request.quantity * Decimal(str(current_stock_specs["buyPrice"]))))
    _record_transaction("purchase", buy_request.ticker, current_stock_specs["countryCode"], buy_request.quantity, Decimal(str(current_stock_specs["buyPrice"])), "USD", user_id)
    
    user_stock = next((s for s in db["users"][user_id].stocks if s.ticker == buy_request.ticker), None)

    if user_stock is None:

        db["users"][user_id].stocks.append(UserStock(
            ticker=buy_request.ticker,
            currency="USD", # USD is the default currency
            countryCode=current_stock_specs["countryCode"],
            quantity=buy_request.quantity
        ))

    else:
        user_stock.quantity += buy_request.quantity



    return BuyStocksResult(
        ticker=buy_request.ticker,
        countryCode=current_stock_specs["countryCode"],
        buyPrice=current_stock_specs["buyPrice"],
        sellPrice=current_stock_specs["sellPrice"]
    )


def _check_user_stock_regulations(user: StoredUser, buy_request: BuyStockMaxPriceRequest, stock_country_code: str):
    regulations_applied = []
    for r in db["regulations"]:
        
        match r["type"]:
            case "full-ban":
                if (r["userCountryCode"] == user.country_code or r["userCountryCode"] == "*") and (r["bannedCountryCode"] == stock_country_code or r["bannedCountryCode"] == "*"):
                    regulations_applied.append(r)
            case "amount-based":
                if r["stockSymbol"] == buy_request.ticker:
                    user_stock_amount = next((s.quantity for s in user.stocks if s.ticker == r["stockSymbol"]), 0) + buy_request.quantity

                    if user_stock_amount > int(r["threshold"]):
                        regulations_applied.append(r)

    return regulations_applied


import threading

purchase_lock = threading.Lock()


def handle_buy_stock_request_max_price(buy_request: BuyStockMaxPriceRequest, user_id: str) -> dict[str, BuyStockMultiCurrencyResult] | JSONResponse:
    current_stock_specs = check_stocks_exists_multi_curr(ticker=buy_request.ticker)
    user = check_user_exists(user_id)

    if Decimal(str(current_stock_specs["buyPrice"])) > buy_request.price:
        raise AppError(Codes.CONFLICT)


    with purchase_lock:
        
        user_stock = next((s for s in user.stocks if s.ticker == buy_request.ticker), None)

        regulations_applied = _check_user_stock_regulations(user, buy_request, current_stock_specs["countryCode"])

        if regulations_applied:

            return JSONResponse(
                status_code=ERRORS[Codes.REGULATION_BLOCKED].status,
                headers={
                    "Link": ", ".join(f"</regulations/{r["id"]}>; rel=\"blocked-by\"" for r in regulations_applied)
                },
                content={
                    "error_code": ERRORS[Codes.REGULATION_BLOCKED].code,
                    "message": ERRORS[Codes.REGULATION_BLOCKED].message
                }
            )
            
        withdraw_money(user_id, Decimal(buy_request.quantity * Decimal(str(current_stock_specs["buyPrice"]))), currency=current_stock_specs["currency"])
        _record_transaction("purchase", buy_request.ticker, current_stock_specs["countryCode"], buy_request.quantity, Decimal(str(current_stock_specs["buyPrice"])), current_stock_specs["currency"], user_id)

        if user_stock is None:

            db["users"][user_id].stocks.append(UserStock(
                ticker=buy_request.ticker,
                currency=current_stock_specs["currency"],
                countryCode=current_stock_specs["countryCode"],
                quantity=buy_request.quantity
            ))

        else:
            user_stock.quantity += buy_request.quantity



    return {
        "stock": BuyStockMultiCurrencyResult(
        ticker=buy_request.ticker,
        countryCode=current_stock_specs["countryCode"],
        buyPrice=current_stock_specs["buyPrice"],
        sellPrice=current_stock_specs["sellPrice"],
        currency=current_stock_specs["currency"],
        name=current_stock_specs["name"]
        )
    }


def handle_sell_stock_request(sell_request: SellStockRequest, user_id: str) -> SellStocksResult:

    current_stock_specs = check_stocks_exists(ticker=sell_request.ticker)

    current_stock_user = next((s for s in db["users"][user_id].stocks if s.ticker == sell_request.ticker), None)

    if current_stock_user is None or sell_request.quantity > current_stock_user.quantity:
        raise AppError(Codes.INSUFFICIENT_QUANTITY)

    elif sell_request.quantity == current_stock_user.quantity:
        db["users"][user_id].stocks.remove(current_stock_user)

    else:
        current_stock_user.quantity -= sell_request.quantity

    deposit_money(user_id, Decimal(sell_request.quantity * Decimal(str(current_stock_specs["sellPrice"]))))

    _record_transaction("sale", sell_request.ticker, current_stock_specs["countryCode"], sell_request.quantity, Decimal(str(current_stock_specs["sellPrice"])), "USD", user_id)

    return SellStocksResult(
        ticker=sell_request.ticker,
        countryCode=current_stock_specs["countryCode"],
        buyPrice=current_stock_specs["buyPrice"],
        sellPrice=current_stock_specs["sellPrice"]
    )


def handle_sell_stock_request_multi_curr(sell_request: SellStockMinPriceRequest, user_id: str) ->  SellStockMultiCurrencyResult:

    current_stock_specs = check_stocks_exists_multi_curr(ticker=sell_request.ticker)

    current_stock_user = next((s for s in db["users"][user_id].stocks if s.ticker == sell_request.ticker), None)

    if Decimal(str(current_stock_specs["sellPrice"])) < sell_request.price:
        raise AppError(Codes.CONFLICT)

    if current_stock_user is None or sell_request.quantity > current_stock_user.quantity:
        raise AppError(Codes.INSUFFICIENT_QUANTITY)

    elif sell_request.quantity == current_stock_user.quantity:
        db["users"][user_id].stocks.remove(current_stock_user)

    else:
        current_stock_user.quantity -= sell_request.quantity

    deposit_money(user_id, Decimal(sell_request.quantity * Decimal(str(current_stock_specs["sellPrice"]))), currency=current_stock_specs["currency"])

    _record_transaction("sale", sell_request.ticker, current_stock_specs["countryCode"], sell_request.quantity, Decimal(str(current_stock_specs["sellPrice"])), current_stock_specs["currency"], user_id)

    return SellStockMultiCurrencyResult(
        ticker=sell_request.ticker,
        countryCode=current_stock_specs["countryCode"],
        buyPrice=current_stock_specs["buyPrice"],
        sellPrice=current_stock_specs["sellPrice"],
        currency=current_stock_specs["currency"],
        name=current_stock_specs["name"]
    )
