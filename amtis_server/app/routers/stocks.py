from fastapi import APIRouter, Query, Depends, Response
from ..models.stocks import StocksFilter, BuyStockRequest, SellStockRequest, BuyStockResponse, SellStockResponse, BuyStockMultiCurrencyResponse, SellStockMultiCurrencyResponse, BuyStockMaxPriceRequest, SellStockMinPriceRequest
from ..services.stocks_handling import filter_stocks, format_stocks, merge_stocks_prices, handle_buy_stock_request, handle_sell_stock_request, handle_buy_stock_request_max_price, handle_sell_stock_request_multi_curr
from typing import Annotated
from ..dependencies.headers import validate_accept_header_format_stocks
from ..adapters.market import market
from ..config import STOCK_FIELDS_V1, STOCK_FIELDS_V2
from ..dependencies.cookies import get_user_id
from dataclasses import asdict
from ..db.store import db


router = APIRouter()


@router.get("/api/stocks")
def get_filtered_stocks(
    filter_query: Annotated[StocksFilter, Query()],
    accept: Annotated[str|None, Depends(validate_accept_header_format_stocks)]
    ):

    stocks = market.get_stocks_prices()
    filtered_stocks = filter_stocks(filter_query, stocks)

    return format_stocks(filtered_stocks, accept, STOCK_FIELDS_V1)


@router.get("/api/v2/stocks")
def get_filtered_stocks_v2(
    filter_query: Annotated[StocksFilter, Query()],
    accept: Annotated[str|None, Depends(validate_accept_header_format_stocks)]
    ):

    stocks = market.get_stocks_v2()
    prices = market.get_prices_v2()

    merged_stocks = merge_stocks_prices(stocks, prices)
    filtered_stocks = filter_stocks(filter_query, merged_stocks)

    return format_stocks(filtered_stocks, accept, STOCK_FIELDS_V2)


@router.get("/api/users/me/stocks/")
def get_user_stocks(
        user_id: Annotated[str, Depends(get_user_id)]
    ):
    
    return {
        "stocks": [{
            "ticker": s.ticker,
            "countryCode": s.countryCode,
            "quantity": s.quantity
        } for s in db["users"][user_id].stocks if s.currency == "USD"]
    }



@router.get("/api/v2/my/stocks")
def get_user_stocks_v2(
    user_id: Annotated[str, Depends(get_user_id)]
):
    return {
        "stocks": [asdict(s) for s in db["users"][user_id].stocks]
    }


@router.post("/api/users/me/stocks/purchases", status_code=201, response_model=BuyStockResponse)
def post_buy_stock(
    user_id: Annotated[str, Depends(get_user_id)],
    buy_request: BuyStockRequest
):
    
    return {
        "stock": handle_buy_stock_request(buy_request, user_id)
    }


@router.post("/api/v2/stocks/purchases", status_code=201,
            response_model=BuyStockMultiCurrencyResponse,
            responses={
                451: {
                    "description": "Purchase blocked by regulation",
                    "content": {
                        "error_code": "code",
                        "message": "error description"
                    },
                    "headers": {
                        "Link": {
                            "description": "References to all flagged regulations",
                            "schema": {"type": "</regulations/[regulation_id]>; rel=\"blocked-by\""}
                        }
                    }
                }
            })
def post_buy_stock_multi_curr(
    user_id: Annotated[str, Depends(get_user_id)],
    buy_request: BuyStockMaxPriceRequest
):
    
    return handle_buy_stock_request_max_price(buy_request, user_id)


@router.post("/api/users/me/stocks/sales", status_code=201, response_model=SellStockResponse)
def post_sell_stock(
    user_id: Annotated[str, Depends(get_user_id)],
    sell_request: SellStockRequest
):
    
    return {
        "stock": handle_sell_stock_request(sell_request, user_id)
    }


@router.post("/api/v2/stocks/sales", status_code=201, response_model=SellStockMultiCurrencyResponse)
def post_sell_stock_multi_curr(
    user_id: Annotated[str, Depends(get_user_id)],
    sell_request: SellStockMinPriceRequest
):
    
    return {
        "stock": handle_sell_stock_request_multi_curr(sell_request, user_id)
    }