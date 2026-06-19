from ..db.store import db
from ..errors.error_codes import Codes
from ..errors.exceptions import AppError
from decimal import Decimal
from ..models.user import UserBalance


def deposit_money(user_id: str, amount: Decimal, currency="USD"):
    balance: Decimal|None = next((b for b in db["users"][user_id].balances if b.currency == currency), None)

    if balance is None:
        db["users"][user_id].balances.append(UserBalance(currency=currency, amount=amount))
    else:
        for b in db["users"][user_id].balances:
            if b.currency == currency:
                b.amount += amount


def withdraw_money(user_id: str, amount: Decimal, currency="USD"):
    balance_amount: Decimal|None = next((b.amount for b in db["users"][user_id].balances if b.currency == currency), None)

    if balance_amount is None or balance_amount < amount:
        raise AppError(Codes.INSUFFICIENT_FUNDS)

    for b in db["users"][user_id].balances:
        if b.currency == currency:
            b.amount -= amount
            break