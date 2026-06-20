from fastapi import APIRouter, Query, Depends
from typing import Annotated
from ..models.forex import ForexQuery, ForexPurchaseQuery
from ..services.forex import exchange_currency, get_exchange_rates
from ..dependencies.cookies import get_user_id


router = APIRouter()


@router.get("/api/forex")
def get_fx_rates(
    fx_query: Annotated[ForexQuery, Query()]
):

    return {
        "rates": get_exchange_rates(fx_query.source, fx_query.to, fx_query.amount)
    }


@router.post("/api/users/me/forex/purchases", status_code=201)
def purchase_fx(
    fx_query: ForexPurchaseQuery,
    user_id: Annotated[str, Depends(get_user_id)]
):

    return exchange_currency(fx_query, user_id)