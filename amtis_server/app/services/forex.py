from ..models.forex import ForexPurchaseQuery
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
from ..services.transactions_handling import withdraw_money, deposit_money
from ..adapters.market import market
from ..errors.error_codes import Codes
from ..errors.exceptions import AppError
from datetime import datetime, timezone
from ..db.store import db


def _record_exchange(source, target, source_amount: Decimal, target_amount: Decimal, user_id: str):

    db["users"][user_id].transactions.append({
        "from": source,
        "to": target,
        "amount": float(str(source_amount)),
        "result": float(str(target_amount)),
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")
    })


def get_exchange_rates(source: str|None, to: str|None, amount: Decimal|None):
    rates = include_reverse_rates(market.get_fx_rates())
    rates = filter_target_rates(rates, source, to)

    if amount is not None:
        rates = calculate_result(rates, amount=amount)

    return rates


def include_reverse_rates(rates: list[dict]) -> list[dict]:
    return rates + [
        {
            "source": r["target"],
            "target": r["source"],
            "rate": float((Decimal("1") / Decimal(str(r["rate"]))).quantize(exp=Decimal("0.001"), rounding=ROUND_DOWN))
        } 
        for r in rates
    ]



def filter_target_rates(rates: list[dict], source: str|None, to: str|None) -> list[dict]:

    return [
        r for r in rates
        if (r["source"] == source or source is None) and ((r["target"] == to or to is None))
    ]


def calculate_result(rates: list[dict], amount: Decimal):
    
    result = []

    for r in rates:
        result.append({**r, "result": float((amount / Decimal(str(r["rate"]))).quantize(Decimal("0.01"), ROUND_HALF_UP))})

    return sorted(result, key=lambda x: -x["result"])


def exchange_currency(fx_query: ForexPurchaseQuery, user_id: str):

    exchanged_money_amount = next((r["result"] for r in get_exchange_rates(fx_query.source, fx_query.to, fx_query.amount) if r["source"] == fx_query.source and r["target"] == fx_query.to), None)

    if exchanged_money_amount is None:
        raise AppError(Codes.INVALID_VALUE) # one of both currencies provided is not supported in the global market

    withdraw_money(amount=fx_query.amount, currency=fx_query.source, user_id=user_id)
    deposit_money(user_id=user_id, amount=Decimal(str(exchanged_money_amount)), currency=fx_query.to)
    _record_exchange(fx_query.source, fx_query.to, fx_query.amount, exchanged_money_amount, user_id)

    return {
        "from": fx_query.source,
        "to": fx_query.to,
        "amount": fx_query.amount,
        "result": exchanged_money_amount
    }